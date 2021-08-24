import graphene
import graphql_jwt
from graphql_jwt.shortcuts import create_refresh_token, get_token
from profiles.models import Profile as profile
from graphql_auth import mutations
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

User = get_user_model()


class AuthorizationError(Exception):
    """Authorization failed."""


## Mutation: Create User
# We want to return:
# - The new `user` entry
# - The new associated `profile` entry - from our extended model
# - The access_token (so that we're automatically logged in)
# - The refresh_token (so that we can refresh my access token)

# Make models available to graphene.Field

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class UserProfile(DjangoObjectType):
    class Meta:
        model = profile


# CreateUser
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    profile = graphene.Field(UserProfile)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, first_name, last_name, username, password, email):
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        profile_obj = profile.objects.get(user=user.id)
        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return CreateUser(user=user, profile=profile_obj, token=token, refresh_token=refresh_token)


# Finalize creating mutation for schema
class AuthMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


## Query: Find users / my own profile
# Demonstrates auth block on seeing all user - only if I'm a manager
# Demonstrates auth block on seeing myself - only if I'm logged in

class AuthQuery(graphene.ObjectType):
    whoami = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_whoami(self, info):
        user = info.context.user
        # Check to to ensure you're signed-in to see yourself
        if user.is_anonymous:
            raise Exception('Authentication Failure: Your must be signed in')
        return user

    def resolve_users(self, info):
        user = info.context.user
        print(user)
        # Check to ensure user is a 'manager' to see all users
        if user.is_anonymous:
            raise Exception('Authentication Failure: Your must be signed in')
        if user.profile.role != 'manager':
            raise Exception('Authentication Failure: Must be Manager')
        return User.objects.all()

import graphene
from graphene_django import DjangoObjectType
# from graphene_django.filter import DjangoFilterConnectionField
from django.conf import settings
from graphql_auth.schema import MeQuery

from django.contrib.auth import get_user_model

from skit.models import Skit
from profiles.models import Profile

from profiles.graphql.schema import ProfileType
from accounts.graphql.schema import AuthMutation, AuthQuery as UserQuery


User = get_user_model()
MEDIA_URL = settings.MEDIA_URL


class AuthorizationError(Exception):
    """Authorization failed."""


class SkitType(DjangoObjectType):
    user = graphene.Field(ProfileType)
    likes = graphene.Int()
    date = graphene.String()
    didlike = graphene.Boolean()
    reposts = graphene.Int()

    class Meta:
        model = Skit

    def resolve_user(self, info, **kwargs):
        qs = Profile.objects.filter(user__username__iexact=self.user).first()
        return qs

    def resolve_image(self, info):
        """Resolve post image absolute path"""
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)
        return self.image

    def resolve_date(self, info, **kwargs):
        months = ["JAN", "FEB", "MARCH", "APR", "MAY",
                  "JUNE", "JULY", "AUG", "SEP", "OCT", "NOV", "DEC"]
        date = f"{months[self.timestamp.date().month].lower()} {self.timestamp.date().day}"
        return date

    def resolve_likes(self, info, **kwargs):
        qs = self.likes.count()
        return qs

    def resolve_didlike(self, info, **kwargs):
        didlike = False
        context = info.context
        if context:
            user = context.user
            didlike = user in self.likes.all()
        return didlike

    def resolve_reposts(self, info, **kwargs):
        qs = Skit.objects.filter(parent_id=self.id).all()
        qs = qs.count()
        return qs


class Query(UserQuery, MeQuery, graphene.ObjectType):
    profile = graphene.List(ProfileType, username=graphene.String())
    skit = graphene.List(SkitType, _id=graphene.Int())
    skits = graphene.List(
        SkitType,
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    feed = graphene.List(SkitType)
    my_profile = graphene.Field(ProfileType)

    def resolve_profile(self, info, username=None):
        try:
            if username:
                return Profile.objects.filter(user__username=username)
        except:
            context = info.context
            user = context.GET.get("username")
            if user:
                return Profile.objects.filter(user__username=user)
            elif not user:
                user = context.user.username
                return Profile.objects.filter(user__username=user)
            else:
                return AuthorizationError("Profile Not Found")

    def resolve_skits(self, info, search=None, first=None, **kwargs):
        location = info.context.user.profile.location
        skits = Skit.objects.by_location(location)
        if not location and not skits.exists():
            skits = Skit.objects.all()

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]
        return skits

    def resolve_skit(self, info, _id, **kwargs):
        qs = Skit.objects.filter(pk=_id)
        print(qs)
        if qs.exists():
            return Skit.objects.filter(pk=_id)
        else:
            return AuthorizationError("Post Not Found")

    def resolve_feed(self, info, **kwargs):
        user = info.context.user
        qs = Skit.objects.feed(user).order_by("-timestamp")
        return qs
    
    def resolve_my_profile(self, info, **kwargs):
        user = info.context.user
        qs = Profile.objects.filter(user=user).first()
        return qs


class SkitMutation(graphene.Mutation):

    class Arguments:
        content = graphene.String(required=True)
        caption = graphene.String(required=True)
    skit = graphene.Field(SkitType)

    @classmethod
    def mutate(cls, root, info, content, caption):
        skit = Skit(caption=caption, content=content, user=info.context.user)
        skit.save()
        return SkitMutation(skit=skit)


class Mutation(AuthMutation, graphene.ObjectType):
    create_skit = SkitMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

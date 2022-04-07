import graphene
from graphene_django import DjangoObjectType
from ..models import Profile, FriendRequest
from accounts.models import User
from graphql_auth.schema import UserQuery


class FriendRequestType(DjangoObjectType):
    count = graphene.Int()
    # sent_request = graphene.List(UserQuery)

    class Meta:
        model = FriendRequest

    def resolve_received_request(self, info, **kwargs):
        context = info.context
        if context:
            user = context.user
            if user.username == self.user.username:
                qs = FriendRequest.objects.filter(to_user=self.user)
            return qs

    def resolve_sent_request(self, info, **kwargs):
        context = info.context
        if context:
            user = context.user
            if user.username == self.user.username:
                qs = FriendRequest.objects.filter(
                    from_user=self.user)
            return qs

    def resolve_count(self, info, **kwargs):
        user = None


class ProfileType(DjangoObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    username = graphene.String()
    email = graphene.String()
    is_following = graphene.Boolean()
    is_friend = graphene.String()
    is_user = graphene.Boolean()

    requests = graphene.List(FriendRequestType)
    received_request = graphene.List(FriendRequestType)
    followers = graphene.List(lambda: ProfileType)

    class Meta:
        model = Profile
        exclude = ["user"]

    def resolve_first_name(self, info, **kwargs):
        try:
            context = info.context
            qs = context.GET.get("username")
            qs = User.objects.filter(username=qs).first().first_name
            if not qs:
                qs = context.user.first_name
            return qs
        except:
            return self.user.first_name

    def resolve_followers(self, info):
        username = self.user.username
        qs = Profile.objects.filter(user__username=username).first().followers.all().values_list('username', flat=True)
        qs = Profile.objects.filter(user__username__in=qs)
        return qs

    def resolve_last_name(self, info, **kwargs):
        try:
            context = info.context
            qs = context.GET.get("username")
            qs = User.objects.filter(username=qs).first().last_name
            if not qs:
                qs = context.user.last_name
            return qs
        except:
            return self.user.last_name

    def resolve_username(self, info, **kwargs):
        context = info.context
        qs = context.GET.get("username")
        if not qs:
            qs = context.user.username
        if not qs:
            qs = self.user.username
        return qs

    def resolve_email(self, info, **kwargs):
        try:
            context = info.context
            qs = context.GET.get("username")
            qs = User.objects.filter(username=qs).first().email
            if not qs:
                qs = context.user.email
            return qs
        except:
            return self.user.email

    def resolve_is_following(self, info, **kwargs):
        is_following = False
        context = info.context
        if context:
            user = context.user
            is_following = user in self.followers.all()
        return is_following

    def resolve_is_friend(self, info, **kwargs):
        is_friend = "none"
        context = info.context
        if context:
            p = Profile.objects.filter(user=self.user).first()
            if context.user.is_authenticated:
                if context.user.profile not in p.friends.all():
                    is_friend = "not_friend"
                    if len(FriendRequest.objects.filter(
                            from_user=context.user).filter(to_user=p.user)) == 1:
                        is_friend = "requested"
                    elif FriendRequest.objects.filter(to_user=context.user, from_user=self.user).exists():
                        is_friend = "requesting"

        return is_friend

    # checking if the current
    # is the same as the obj user
    def resolve_is_user(self, info):
        is_user = False
        context = info.context
        user = context.user
        if user:
            if user.username == context.user.username:
                is_user = True
        else:
            if self.user.username == context.user.username:
                is_user = True
        return is_user

    def resolve_requests(self, info, **kwargs):
        username = info.context.user.username
        qs = Profile.objects.filter(user__username=username)
        return qs

    def resolve_received_request(self, info, **kwargs):
        username = info.context.user.username
        # if username == self.user.username:
        qs = FriendRequest.objects.filter(to_user__username=username)
        print(qs)
        qs_list = []
        for qs in qs:
            qs = Profile.objects.filter(user__username=qs.from_user.username)
            print(qs)

        return qs

    def resolve_image(self, info):
        """Resolve post image absolute path"""
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)
        return self.image

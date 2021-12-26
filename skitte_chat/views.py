from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View
from .forms import ThreadForm, MessageForm
from .models import PrivateMessageModel, PrivateThreadModel, PublicChatRoom, PublicRoomChatMessage
from django.contrib import messages
from accounts.models import User
from profiles.models import Profile
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'chat/index.html', {})


def room_redirect(request, room_name):
    try:
        qs = PublicChatRoom.objects.filter(
            title=room_name, created_by=request.user, users=request.user, admins=request.user)
        if not qs.exists():
            qs = PublicChatRoom.objects.create(
                title=room_name, created_by=request.user)
            qs.save()
            qs = PublicChatRoom.objects.filter(
                title=room_name, created_by=request.user)
            slug = qs.first().slug
            for qs in qs:
                qs.users.add(request.user)
                qs.admins.add(request.user)
        return redirect("chatroom", room_name=room_name, slug=slug)
    except:
        print("error ohh")


def chat_room(request, room_name, slug):
    qs = PublicChatRoom.objects.filter(title=room_name, slug=slug)
    me = request.user

    in_group = PublicChatRoom.check_if_user_is_from_room(
        PublicChatRoom, slug, me)

    print(in_group)

    if not qs.exists():
        return redirect("room", room_name=room_name)

    return render(request, 'chatapp/room.html', {
        'room_name': room_name,
        'id': qs.first().id,
        'slug': slug,
        'in_group': in_group
    })


class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = PrivateThreadModel.objects.filter(
            Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, 'inbox/inbox.html', context)


class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }

        return render(request, 'inbox/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username=username)
            if PrivateThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = PrivateThreadModel.objects.filter(
                    user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif PrivateThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = PrivateThreadModel.objects.filter(
                    user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = PrivateThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            messages.error(request, 'Invalid username')
            return redirect('create-thread')


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = PrivateThreadModel.objects.get(pk=pk)
        message_list = PrivateMessageModel.objects.filter(
            thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'inbox/thread.html', context)


class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = PrivateThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()

        # notification = Notification.objects.create(
        #     notification_type=4,
        #     from_user=request.user,
        #     to_user=receiver,
        #     thread=thread
        # )
        # return redirect('thread', pk=pk)
        return HttpResponse("success")


# this view is the base view
def chat_index(request):

    # UNCOMMENT THE LINES BEFORE IF YOU WANT THE APP TO DELETE SOME MESSAGES WHEN THERE ARE MANY

    # ------ counts the existing messages on db
    #msgsLen = Message.objects.all().count()

    # ------ if there are more than 100 messages, deletes the first four hundred messages
    # if msgsLen > 500:
    #    for message in Message.objects.all()[:400]:
    #        message.delete()

    # passes all the messages to the context
    context = {
        'messages': PublicRoomChatMessage.objects.all()
    }

    # and returns it to the page
    return render(request, 'test.html', context)

# this view must be csrf exempted to be able to accept XMLHttpRequests


@csrf_exempt
def save_message(request):
    # if the request method is a POST request
    if request.method == 'POST':
        # content sent via XMLHttpRequests can be accessed in request.body
        # and it comes in a JSON string, that's why we use json library to
        # turn it into a normal dictionary again
        msg_obj = json.loads(request.body.decode('utf-8'))

        # tries to create the message and save it in the db
        try:
            msg = Message.objects.create(
                user_name=msg_obj['user_name'], message=msg_obj['message'])
            msg.save()
        # if some error occurs it will print the error in the django console and return a HttpResponse
        # containing a error value, which will be received by nodejs socket.io
        except:
            print("error saving message")
            return HttpResponse("error")

        # if there aren't any errors, it returns a HttpResponse containing a success value, which will
        # be received by nodejs socket.io
        return HttpResponse("success")

    # if it is a GET request (someone trying to access to the link or something)
    # returns to the main page without doing anything
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def save_dm(request, pk):
    form = MessageForm(request.POST, request.FILES)
    thread = PrivateThreadModel.objects.get(pk=pk)
    if thread.receiver == request.user:
        receiver = thread.user
    else:
        receiver = thread.receiver

    if form.is_valid():
        message = form.save(commit=False)
        message.thread = thread
        message.sender_user = request.user
        message.receiver_user = receiver
        message.save()
        return HttpResponse("success")

    # if it is a GET request (someone trying to access to the link or something)
    # returns to the main page without doing anything
    else:
        return HttpResponseRedirect('/')



def get_last_10_messages(chatId):
    chat = get_object_or_404(PublicChatRoom, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Profile, user=user)


def get_current_chat(chatId):
    return get_object_or_404(PublicChatRoom, id=chatId)

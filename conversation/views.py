from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from posh.models import RecruitUser, IndividualUser, EstablishmentUser

from .forms import ConversationMessageForm
from .models import Conversation

@login_required
def new_conversation(request, pk):
    user = get_object_or_404(RecruitUser, pk=pk)
    # print(user.id)
    # print(request.user)
    # print(user.establishment_id)
    # print(user.user_id)
    
    conversations = Conversation.objects.filter(est=user).filter(members=[user.user_id])

    if conversations:
        pass # redirect to conversation

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(est=user)
            conversation.members.add(request.user)
            conversation.members.add(user.user_id)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('conversation:inbox')

    else:
        form = ConversationMessageForm()
    
    return render(request, 'new.html',{
        'form':form
    })

@login_required
def inbox(request):
    user = request.user
    individual_users = []
    conversations = Conversation.objects.filter(members=user).prefetch_related('members')

    for conv in conversations:
        for member in conv.members.all():
            if member != user:  
                try:
                    if str(member).startswith("ES"):
                        individual_user = EstablishmentUser.objects.get(username=member)
                        user_info = {
                            'name': individual_user.name,
                            'city': individual_user.city,
                            'state': individual_user.state,
                            'modified_at': conv.modified_at,
                            'id': conv.id,
                        }
                        if user_info not in individual_users:  # Check for duplicates
                            individual_users.append(user_info)
                    if str(member).startswith("IN"):
                        individual_user = IndividualUser.objects.get(username=member)
                        user_info = {
                            'fname': individual_user.fname,
                            'lname': individual_user.lname,
                            'city': individual_user.city,
                            'state': individual_user.state,
                            'modified_at': conv.modified_at,
                            'id': conv.id,
                        }
                        if user_info not in individual_users:  # Check for duplicates
                            individual_users.append(user_info)
                except IndividualUser.DoesNotExist:
                    continue  # Skip if the IndividualUser does not exist

    return render(request, 'inbox.html', {
        'conversations': conversations,
        'individual_users': individual_users
    })

@login_required
def detail(request, pk):
    user = request.user
    conversation = Conversation.objects.filter(members=user).get(pk=pk)

    if str(user).startswith("ES"):
        est_name = EstablishmentUser.objects.get(username=request.user)
        user_name = IndividualUser.objects.get(username=conversation.est.user_id)
        user_name.name = user_name.fname + user_name.lname
    elif str(user).startswith("IN"):
        est_name = IndividualUser.objects.get(username=request.user)
        est_name.name = est_name.fname + est_name.lname
        user_name = EstablishmentUser.objects.get(username=conversation.est.establishment_id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'detail.html', {
        'conversation': conversation,
        'est_name': est_name,
        'user_name': user_name,
        'form': form
    })
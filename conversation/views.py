from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from posh.models import RecruitUser, IndividualUser

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

            return redirect('conversation:new', pk=pk)

    else:
        form = ConversationMessageForm()
    
    return render(request, 'new.html',{
        'form':form
    })

@login_required
def inbox(request):
    user = request.user
    individual_users = []

    print(f"Username: {user.username}")
    # Prefetch related members to reduce queries
    conversations = Conversation.objects.filter(members=user).prefetch_related('members')
    
    print(f"User's conversations: {conversations}")
    for conv in conversations:
        print(f"Conversation ID: {conv.id}, Members: {[member.username for member in conv.members.all()]}")
    
    # Collect individual users once
    for conv in conversations:
        for member in conv.members.all():
            if member != user:
                try:
                    individual_user = IndividualUser.objects.get(username=member)
                    user_info = {
                        'fname': individual_user.fname,
                        'lname': individual_user.lname,
                        'city': individual_user.city,
                        'state': individual_user.state,
                        'modified_at': conv.modified_at
                    }
                    if user_info not in individual_users:  # Check for duplicates
                        individual_users.append(user_info)
                except IndividualUser.DoesNotExist:
                    continue  # Skip if the IndividualUser does not exist
    
    print(individual_users)
    return render(request, 'inbox.html', {
        'conversations': conversations,
        'individual_users': individual_users
    })
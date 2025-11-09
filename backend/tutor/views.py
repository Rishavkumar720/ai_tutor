import os
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from .models import ChatHistory, QuizResult, UserProgress
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout


# Load API Key
GROQ_API_KEY = settings.GROQ_API_KEY

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY NOT FOUND.")

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile"
)


@login_required
def tutor_view(request):
    explanation = None
    quiz = request.session.get("quiz")
    result = None

    if request.method == "POST":
        action = request.POST.get("action")

        # ----------------------------------------------------
        # ✅ Generate Explanation
        # ----------------------------------------------------
        if action == "explain":
            topic = request.POST.get("topic")

            messages = [
                SystemMessage(content="Explain the topic in clean, safe HTML without styling."),
                HumanMessage(content=f"Explain {topic} in HTML format.")
            ]

            response = llm.invoke(messages)
            explanation = response.content

            ChatHistory.objects.create(
                user=request.user,
                topic=topic,
                response=explanation
            )

            # ----------------------------------------------------
            # ✅ Create 3-Question Quiz
            # ----------------------------------------------------
            quiz_prompt = [
                SystemMessage(content="Return ONLY valid JSON."),
                HumanMessage(content=f"""
                Create 3 MCQ questions for {topic}.
                Return JSON exactly like this:

                [
                    {{
                        "question": "...",
                        "options": ["A", "B", "C", "D"],
                        "answer": "A"
                    }},
                    {{
                        "question": "...",
                        "options": ["A", "B", "C", "D"],
                        "answer": "B"
                    }},
                    {{
                        "question": "...",
                        "options": ["A", "B", "C", "D"],
                        "answer": "C"
                    }}
                ]
                """)
            ]

            quiz_response = llm.invoke(quiz_prompt)

            try:
                quiz_list = json.loads(quiz_response.content)
                request.session["quiz"] = quiz_list
                quiz = quiz_list

            except json.JSONDecodeError:
                quiz = None
                request.session["quiz"] = None

        # ----------------------------------------------------
        # ✅ Submit Quiz Answer
        # ----------------------------------------------------
        elif action == "submit_quiz":
            quiz = request.session.get("quiz")

            if not quiz:
                result = "Quiz not found. Generate a topic again."
            else:
                # Identify which question user answered
                question_index = int(request.POST.get("question_index"))
                current_q = quiz[question_index]

                user_answer = request.POST.get("user_answer")
                correct_answer = current_q["answer"]

                is_correct = user_answer == correct_answer

                # Save result
                QuizResult.objects.create(
                    user=request.user,
                    question=current_q["question"],
                    user_answer=user_answer,
                    correct_answer=correct_answer,
                    is_correct=is_correct
                )

                progress, created = UserProgress.objects.get_or_create(user=request.user)
                progress.total_questions += 1
                if is_correct:
                    progress.correct_answers += 1
                progress.save()

                result = "✅ Correct!" if is_correct else f"❌ Wrong. Correct answer: {correct_answer}"

    return render(request, "tutor.html", {
        "explanation": explanation,
        "quiz": quiz,
        "result": result,
    })


# ✅ Dashboard
@login_required
def dashboard(request):
    chats = ChatHistory.objects.filter(user=request.user).order_by("-created_at")
    quizzes = QuizResult.objects.filter(user=request.user).order_by("-created_at")
    progress = UserProgress.objects.filter(user=request.user).first()

    return render(request, "dashboard.html", {
        "chats": chats,
        "quizzes": quizzes,
        "progress": progress,
    })



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("tutor")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")


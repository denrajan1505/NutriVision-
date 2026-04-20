import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import base64
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# ✅ Page config
st.set_page_config(
    page_title="Food Nutrition Analyzer",
    page_icon="🥗",
    layout="wide"
)

# Initialize the LLM
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4o",
    temperature=0.2
)

# ── Helper: Convert image to base64 ─────────────────────────────────────────
def encode_image(uploaded_file) -> str:
    return base64.b64encode(uploaded_file.read()).decode("utf-8")

# ── Helper: Analyze food image using GPT-4o Vision ──────────────────────────
def analyze_food(base64_image: str, file_type: str, goal: str, dietary: str) -> str:
    from langchain_core.messages import HumanMessage

    message = HumanMessage(content=[
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/{file_type};base64,{base64_image}"
            }
        },
        {
            "type": "text",
            "text": f"""
            You are an expert nutritionist and dietitian.
            Carefully analyze this food image and provide the following:

            User Health Goal : {goal}
            Dietary Preference: {dietary}

            1. FOOD IDENTIFICATION
               - Identify all food items visible in the image
               - Estimate portion sizes

            2. NUTRITION BREAKDOWN (per serving)
               - Calories
               - Protein (g)
               - Carbohydrates (g)
               - Fats (g)
               - Fiber (g)
               - Sugar (g)
               - Sodium (mg)
               - Key Vitamins and Minerals

            3. HEALTH SCORE
               - Give an overall health score out of 10
               - Explain why you gave that score

            4. GOAL ALIGNMENT
               - Is this food suitable for the user's goal: {goal}?
               - How does it help or hinder their goal?

            5. DIETARY COMPATIBILITY
               - Is it compatible with {dietary} diet?
               - Any allergens present?

            6. BENEFITS & CONCERNS
               - Top 3 health benefits of this meal
               - Top 3 concerns or things to watch out for

            7. HEALTHIER ALTERNATIVES
               - Suggest 3 healthier alternatives or modifications
               - How to make this meal more nutritious

            8. MEAL TIMING SUGGESTION
               - Best time to eat this meal (breakfast/lunch/dinner/snack)
               - Why it suits that time

            Format clearly with headings and bullet points.
            Use simple, easy-to-understand language.

            ⚠️ DISCLAIMER: This is an AI-assisted analysis.
            Consult a registered dietitian for personalized nutrition advice.
            """
        }
    ])

    response = llm.invoke([message])
    return response.content

# ── Helper: Generate meal plan based on analysis ────────────────────────────
def generate_meal_plan(analysis: str, goal: str) -> str:
    meal_plan_prompt = PromptTemplate(
        input_variables=["analysis", "goal"],
        template="""
        Based on this food analysis:
        {analysis}

        And the user's health goal: {goal}

        Create a simple 1-day meal plan that:
        1. Complements the analyzed food
        2. Helps achieve the user's goal
        3. Is balanced and practical

        Format as:
        BREAKFAST: ...
        MORNING SNACK: ...
        LUNCH: ...
        EVENING SNACK: ...
        DINNER: ...

        Also provide total estimated daily calories.
        Keep it simple and practical.
        """
    )
    meal_chain = meal_plan_prompt | llm | StrOutputParser()
    return meal_chain.invoke({"analysis": analysis, "goal": goal})

# ── UI ────────────────────────────────────────────────────────────────────────
st.title("🥗 Food Nutrition Analyzer")
st.write("Upload a food image and get a complete nutrition breakdown and health insights.")
st.markdown("---")

# ── Sidebar: User Preferences ────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Your Preferences")
    st.markdown("---")

    health_goal = st.selectbox(
        "🎯 Health Goal",
        [
            "Weight Loss",
            "Muscle Gain",
            "Maintain Weight",
            "Improve Energy",
            "Heart Health",
            "Diabetes Management",
            "General Wellness"
        ]
    )

    dietary_pref = st.selectbox(
        "🥦 Dietary Preference",
        [
            "No Restriction",
            "Vegetarian",
            "Vegan",
            "Keto",
            "Gluten Free",
            "Dairy Free",
            "Low Carb",
            "High Protein"
        ]
    )

    show_meal_plan = st.checkbox("📅 Generate 1-Day Meal Plan", value=True)

    st.markdown("---")
    st.info("💡 Tip: Use clear, well-lit food images for best results.")

# ── Main Layout ───────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📸 Upload Food Image")
    uploaded_file = st.file_uploader(
        "Upload food image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Supported: JPG, JPEG, PNG, WEBP"
    )

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Food Image", use_column_width=True)
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        st.markdown("---")

        # Show selected preferences
        st.markdown("**Your Preferences:**")
        st.markdown(f"🎯 Goal: **{health_goal}**")
        st.markdown(f"🥦 Diet: **{dietary_pref}**")

        analyze_btn = st.button("🔍 Analyze Nutrition", use_container_width=True)

with col2:
    st.subheader("📊 Nutrition Analysis")

    if uploaded_file and analyze_btn:

        # ── Nutrition Analysis ──
        with st.spinner("Analyzing food nutrition..."):
            uploaded_file.seek(0)
            file_ext   = uploaded_file.name.split(".")[-1].lower()
            base64_img = encode_image(uploaded_file)
            result     = analyze_food(base64_img, file_ext, health_goal, dietary_pref)

        # Display result
        st.markdown(
            f"""
            <div style="
                background-color: #f0fff4;
                border: 1px solid #b2dfdb;
                border-radius: 10px;
                padding: 25px 30px;
                font-family: Arial, sans-serif;
                font-size: 14px;
                line-height: 1.8;
                color: #1a1a2e;
                white-space: pre-wrap;
                max-height: 500px;
                overflow-y: auto;
            ">{result}</div>
            """,
            unsafe_allow_html=True
        )

        # ── Download Analysis ──
        st.markdown("### ⬇️ Download Analysis")
        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button(
                label="📄 Download as TXT",
                data=result,
                file_name="nutrition_analysis.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col_b:
            st.download_button(
                label="📋 Download as MD",
                data=result,
                file_name="nutrition_analysis.md",
                mime="text/markdown",
                use_container_width=True
            )

        # ── Meal Plan Section ──
        if show_meal_plan:
            st.markdown("---")
            st.subheader("📅 Your 1-Day Meal Plan")
            with st.spinner("Generating personalized meal plan..."):
                meal_plan = generate_meal_plan(result, health_goal)

            st.markdown(
                f"""
                <div style="
                    background-color: #fff8e1;
                    border: 1px solid #ffe082;
                    border-radius: 10px;
                    padding: 25px 30px;
                    font-family: Arial, sans-serif;
                    font-size: 14px;
                    line-height: 1.8;
                    color: #1a1a2e;
                    white-space: pre-wrap;
                ">{meal_plan}</div>
                """,
                unsafe_allow_html=True
            )

            st.download_button(
                label="📅 Download Meal Plan",
                data=meal_plan,
                file_name="meal_plan.txt",
                mime="text/plain",
                use_container_width=True
            )

    elif not uploaded_file:
        st.info("👈 Please upload a food image to get started.")

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown("---")
st.warning("""
⚠️ **Nutrition Disclaimer:** This app provides AI-estimated nutrition information.
Values are approximate and may vary based on preparation methods and portion sizes.
Consult a registered dietitian for personalized nutrition advice.
""")
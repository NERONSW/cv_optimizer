import os
import streamlit as st
from openai import OpenAI

# ------------------------------------------------------------------------------
# 1. Page Configuration & Setup
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="CV & Cover Letter Tailor", page_icon="📄", layout="wide"
)


def load_file(filename: str) -> str | None:
    """Safely load a local markdown/text file."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None


def validate_openrouter_key(api_key: str) -> bool:
    """Verify OpenRouter API key with a lightweight models.list call."""
    try:
        test_client = OpenAI(
            base_url="https://openrouter.ai/api/v1", api_key=api_key
        )
        test_client.models.list()
        return True
    except Exception:
        return False


# ------------------------------------------------------------------------------
# 2. Session State Initialization
# ------------------------------------------------------------------------------
if "key_valid" not in st.session_state:
    # Check for existing environment variable or Streamlit secret
    env_key = os.getenv("OPENROUTER_API_KEY", "") or st.secrets.get(
        "OPENROUTER_API_KEY", ""
    )
    if env_key and validate_openrouter_key(env_key):
        st.session_state["api_key"] = env_key
        st.session_state["key_valid"] = True
    else:
        st.session_state["api_key"] = ""
        st.session_state["key_valid"] = False

# ------------------------------------------------------------------------------
# 3. Sidebar: Authentication & Configuration
# ------------------------------------------------------------------------------
with st.sidebar:
    st.title("📄 CV Tailor Config")
    st.header("🔑 1. API Authentication")

    if st.session_state["key_valid"]:
        st.success("API Key Verified")
        if st.button("Reset / Change Key"):
            st.session_state["key_valid"] = False
            st.session_state["api_key"] = ""
            st.rerun()
    else:
        st.warning("Enter a valid OpenRouter API Key to unlock options.")
        input_key = st.text_input(
            "OpenRouter API Key:", type="password", key="key_input"
        )
        if st.button("Validate Key", type="primary", use_container_width=True):
            if input_key.strip():
                with st.spinner("Validating API key..."):
                    if validate_openrouter_key(input_key.strip()):
                        st.session_state["api_key"] = input_key.strip()
                        st.session_state["key_valid"] = True
                        st.success("Key validated successfully!")
                        st.rerun()
                    else:
                        st.error(
                            "Invalid API Key. Please verify your OpenRouter key."
                        )
            else:
                st.error("Key field cannot be empty.")

    # Options unlocked ONLY if API key is valid
    if st.session_state["key_valid"]:
        st.divider()
        st.header("⚙️ 2. Model Selection")
        model = st.selectbox(
            "Select OpenRouter Model",
            options=[
                "openai/gpt-4o-mini",
                "deepseek/deepseek-chat",
                "google/gemini-2.5-flash",
                "anthropic/claude-3.5-sonnet",
            ],
            index=0,
            help="DeepSeek and GPT-4o-mini offer great performance and low cost.",
        )

        st.divider()
        st.header("🎯 3. CV Format Strategy")

        # Approach Selection (Default: Project-based)
        cv_approach = st.radio(
            "Select Structuring Approach:",
            options=["Project-based", "Role-based"],
            index=0,  # Default selection is Project-based
            help="Project-based focuses on major projects and tech stacks. Role-based structures chronologically by job position.",
        )

        st.divider()
        st.header("📏 4. Layout & Rules Overrides")

        # Load local prompt and resume files
        prompt_project = load_file("master_prompt_project_based.md")
        prompt_role = load_file("master_prompt_role_based.md")
        resume_content = load_file("master_resume.md")
        cover_letter_content = load_file("master_cover_letter.md")
        common_cv_content = load_file("common_cv_template.md")

        # Determine active prompt file based on user selection
        if cv_approach == "Project-based":
            active_prompt_content = prompt_project
            active_prompt_filename = "master_prompt_project_based.md"
        else:
            active_prompt_content = prompt_role
            active_prompt_filename = "master_prompt_role_based.md"

        use_exemplar = st.checkbox(
            "Use 2-Page CV Template as Structural Exemplar",
            value=True if common_cv_content else False,
            disabled=not bool(common_cv_content),
            help="Uses common_cv_template.md as a target layout and word count budget.",
        )
        strict_2_page = st.checkbox(
            "Enforce Strict 2-Page Budget Rules",
            value=True,
            help="Injects hard word and bullet count limits.",
        )
        summary_lines = st.slider(
            "Summary Line Limit", min_value=1, max_value=8, value=4
        )
        extra_instructions = st.text_area(
            "Custom Goal / Role Directive (Optional):",
            placeholder="e.g., Highlight AWS cloud practitioner certification & FinTech project experience...",
            height=80,
        )

        st.divider()
        st.header("📁 5. Local Files Status")
        st.write(
            "🟢 `master_prompt_project_based.md`"
            if prompt_project
            else "🔴 `master_prompt_project_based.md` (Missing)"
        )
        st.write(
            "🟢 `master_prompt_role_based.md`"
            if prompt_role
            else "🔴 `master_prompt_role_based.md` (Missing)"
        )
        st.write(
            "🟢 `master_resume.md`"
            if resume_content
            else "🔴 `master_resume.md` (Missing)"
        )
        st.write(
            "🟢 `common_cv_template.md`"
            if common_cv_content
            else "⚪ `common_cv_template.md` (Optional Exemplar)"
        )
        st.write(
            "🟢 `master_cover_letter.md`"
            if cover_letter_content
            else "⚪ `master_cover_letter.md` (Optional)"
        )

# ------------------------------------------------------------------------------
# 4. Main UI & Application Logic
# ------------------------------------------------------------------------------
st.title("📄 Local CV & Cover Letter Tailor")

# Gatekeeper: Block if API key is not valid
if not st.session_state["key_valid"]:
    st.info(
        "👈 **Please enter and validate your OpenRouter API Key in the sidebar to unlock the application.**"
    )
    st.stop()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Target Job Description")
    st.caption(
        f"Active Strategy: **{cv_approach}** (using `{active_prompt_filename}`)"
    )

    job_description = st.text_area(
        "Paste the Job Description here:",
        height=460,
        placeholder="Paste full job description including responsibilities, mandatory requirements, and tech stack...",
    )

    generate_btn = st.button(
        f"🚀 Generate Tailored Package ({cv_approach})",
        type="primary",
        use_container_width=True,
    )

with col2:
    st.subheader("Tailored Output & Analysis")

    if generate_btn:
        # Validate active local files
        if not active_prompt_content or not resume_content:
            st.error(
                f"Missing required local files! Ensure `{active_prompt_filename}` and `master_resume.md` exist in your project folder."
            )
        elif not job_description.strip():
            st.warning("Please paste a target Job Description on the left.")
        else:
            # 1. Build Dynamic System Prompt Overrides
            custom_rules = f"\n\n====================================================\nDYNAMIC RULE OVERRIDES (HIGHEST PRIORITY)\n====================================================\n"
            custom_rules += (
                f"- SELECTED APPROACH STRATEGY: {cv_approach.upper()}\n"
            )
            custom_rules += f"- PROFESSIONAL SUMMARY LINE LIMIT: Max {summary_lines} lines.\n"

            if strict_2_page:
                custom_rules += (
                    "- STRICT TWO-PAGE BUDGET: Keep total resume under 800-850 words. "
                    "Ensure bullet lengths remain 1-2 lines each (15-25 words max).\n"
                )

            if extra_instructions.strip():
                custom_rules += (
                    f"- CUSTOM USER DIRECTIVE: {extra_instructions.strip()}\n"
                )

            final_system_prompt = active_prompt_content + custom_rules

            # 2. Build User Context Payload (including optional Exemplar)
            exemplar_block = ""
            if use_exemplar and common_cv_content:
                exemplar_block = f"""
====================================================
STRUCTURAL TARGET (2-PAGE COMMON CV TEMPLATE)
====================================================
Use the exact visual density, section proportions, bullet counts, and layout constraints of this exemplar as your target budget:

{common_cv_content}
"""

            user_payload = f"""
{exemplar_block}

====================================================
1. MASTER RESUME (SOURCE OF TRUTH)
====================================================
Extract technical facts, project experience, and achievements ONLY from here:

{resume_content}

====================================================
2. MASTER COVER LETTER
====================================================
{cover_letter_content if cover_letter_content else "No master cover letter provided. Generate cover letter from Master Resume facts."}

====================================================
3. JOB DESCRIPTION
====================================================
{job_description}
"""

            # 3. Call OpenRouter API
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=st.session_state["api_key"],
            )

            with st.spinner(
                f" tailoring package ({cv_approach}) using `{model}`..."
            ):
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": final_system_prompt},
                            {"role": "user", "content": user_payload},
                        ],
                        temperature=0.2,
                    )

                    result_text = response.choices[0].message.content
                    st.success(
                        f"Optimization Complete! Format: {cv_approach}"
                    )

                    # Display formatted result
                    st.markdown(result_text)

                    st.divider()
                    st.download_button(
                        label=f"💾 Download Tailored Package ({cv_approach} .md)",
                        data=result_text,
                        file_name=f"tailored_cv_{cv_approach.lower().replace('-', '_')}.md",
                        mime="text/markdown",
                        use_container_width=True,
                    )

                except Exception as e:
                    st.error(f"API Request Failed: {str(e)}")
    else:
        st.info(
            "Paste the target Job Description on the left and click **Generate Tailored Package**."
        )
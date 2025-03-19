import openai
import streamlit as st

# Function to generate posts with the new requirements
def generate_post(content_topic, tone, content_purpose, api_key):
    client = openai.OpenAI(api_key=api_key)
    
    prompt = f"""Generate social media posts about: '{content_topic}'. 
    Purpose: {content_purpose}
    
    Requirements:
    1. LinkedIn: A {tone} post of at least 200 words with appropriate emojis and hashtags.
    2. Twitter: A concise {tone} post with emojis and hashtags (within character limit).
    3. WhatsApp: A {tone} message with emojis that can be easily shared.
    
    Include emojis naturally throughout all posts to enhance engagement."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = response.choices[0].message.content.strip()
        sections = text.split("\n\n")
        
        # Process the response to separate the different posts
        linkedin_post = ""
        twitter_post = ""
        whatsapp_post = ""
        
        current_section = ""
        for section in sections:
            lower_section = section.lower()
            if "linkedin" in lower_section and len(linkedin_post) == 0:
                linkedin_post = section
            elif "twitter" in lower_section and len(twitter_post) == 0:
                twitter_post = section
            elif "whatsapp" in lower_section and len(whatsapp_post) == 0:
                whatsapp_post = section
            elif len(linkedin_post) > 0 and len(twitter_post) == 0:
                linkedin_post += "\n\n" + section
            elif len(twitter_post) > 0 and len(whatsapp_post) == 0:
                twitter_post += "\n\n" + section
            elif len(whatsapp_post) > 0:
                whatsapp_post += "\n\n" + section
        
        return {
            "linkedin": linkedin_post if linkedin_post else "LinkedIn post not generated.",
            "twitter": twitter_post if twitter_post else "Twitter post not generated.",
            "whatsapp": whatsapp_post if whatsapp_post else "WhatsApp post not generated."
        }
    except Exception as e:
        return {
            "error": str(e),
            "linkedin": "",
            "twitter": "",
            "whatsapp": ""
        }

# Streamlit UI
st.set_page_config(page_title="Social Media Content Generator", layout="wide")

st.title("📢 Social Media Content Generator")
st.markdown("Generate AI-powered content for LinkedIn, Twitter, and WhatsApp!")

# API Key input with password masking
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

# Content details
content_topic = st.text_area("📝 What would you like to post about?", "", height=100)
tone = st.selectbox("🎭 Tone", ["Professional", "Casual", "Exciting", "Formal", "Informative"])
content_purpose = st.selectbox("🎯 Content Purpose", [
    "Sharing industry news",
    "Promoting a product/service",
    "Sharing personal achievement",
    "Company update",
    "Thought leadership",
    "Educational content"
])

# Generate Button
if st.button("🚀 Generate Posts"):
    if not api_key:
        st.error("⚠️ Please enter your OpenAI API Key!")
    elif not content_topic:
        st.warning("⚠️ Please enter a topic for your posts!")
    else:
        with st.spinner("Generating your posts..."):
            posts = generate_post(
                content_topic, 
                tone, 
                content_purpose,
                api_key
            )
            
            if "error" in posts and posts["error"]:
                st.error(f"Error: {posts['error']}")
            else:
                # Display posts in expandable sections
                with st.expander("📌 LinkedIn Post", expanded=True):
                    st.markdown(posts["linkedin"])
                    if st.button("📋 Copy LinkedIn Post"):
                        st.code(posts["linkedin"], language="")
                
                with st.expander("🐦 Twitter Post", expanded=True):
                    st.markdown(posts["twitter"])
                    if st.button("📋 Copy Twitter Post"):
                        st.code(posts["twitter"], language="")
                
                with st.expander("💬 WhatsApp Post", expanded=True):
                    st.markdown(posts["whatsapp"])
                    if st.button("📋 Copy WhatsApp Post"):
                        st.code(posts["whatsapp"], language="")
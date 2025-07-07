"""Mini Project 2: SequentialChain for Content Pipeline."""

import streamlit as st
from langchain.chains import SequentialChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from config import lmstudio_config
from utils import format_error_message
from styles import MAIN_CSS
import logging

logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Mini Project 2: Sequential Chain Pipeline",
    page_icon="🔗",
    layout="wide"
)

# Apply custom CSS
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# Page header
st.markdown('<h1 class="main-header">🔗 Mini Project 2: Sequential Chain Pipeline</h1>', unsafe_allow_html=True)
st.markdown("*Chain multiple LLM operations together to build complex content generation workflows.*")
st.markdown("---")


class ContentPipeline:
    """Sequential chain pipeline for content generation."""
    
    def __init__(self):
        self.llm = None
        self.pipeline = None
        self._setup_llm()
        self._setup_pipeline()
    
    def _setup_llm(self):
        """Initialize the LLM."""
        base_url = st.session_state.get("base_url", lmstudio_config.base_url)
        model = st.session_state.get("model", lmstudio_config.model)
        temperature = st.session_state.get("temperature", lmstudio_config.temperature)
        
        try:
            self.llm = ChatOpenAI(
                base_url=f"{base_url}/v1",
                api_key=lmstudio_config.api_key,
                model=model,
                temperature=temperature,
                timeout=lmstudio_config.timeout
            )
        except Exception as e:
            st.error(f"Failed to initialize LLM: {format_error_message(e)}")
    
    def _setup_pipeline(self):
        """Setup the sequential chain pipeline."""
        if not self.llm:
            return
        
        try:
            # Chain 1: Blog Post Generation
            blog_prompt = PromptTemplate(
                input_variables=["topic", "tone", "length"],
                template="""
                Write a {length} blog post about "{topic}" in a {tone} tone.
                
                Structure the post with:
                - An engaging introduction
                - Main content with key points
                - A compelling conclusion
                
                Make it informative and well-structured.
                """
            )
            
            blog_chain = LLMChain(
                llm=self.llm,
                prompt=blog_prompt,
                output_key="blog_post",
                verbose=True
            )
            
            # Chain 2: Summary Generation
            summary_prompt = PromptTemplate(
                input_variables=["blog_post"],
                template="""
                Create a concise summary of the following blog post in 2-3 sentences.
                Focus on the main points and key takeaways.
                
                Blog Post:
                {blog_post}
                
                Summary:
                """
            )
            
            summary_chain = LLMChain(
                llm=self.llm,
                prompt=summary_prompt,
                output_key="summary",
                verbose=True
            )
            
            # Chain 3: SEO Keywords Extraction
            keywords_prompt = PromptTemplate(
                input_variables=["blog_post"],
                template="""
                Extract 8-12 relevant SEO keywords from the following blog post.
                Focus on terms that would help people find this content.
                
                Format as a comma-separated list.
                
                Blog Post:
                {blog_post}
                
                SEO Keywords:
                """
            )
            
            keywords_chain = LLMChain(
                llm=self.llm,
                prompt=keywords_prompt,
                output_key="keywords",
                verbose=True
            )
            
            # Chain 4: Social Media Posts
            social_prompt = PromptTemplate(
                input_variables=["blog_post", "summary"],
                template="""
                Create social media posts to promote this blog post:
                
                Blog Summary: {summary}
                
                Create:
                1. A Twitter/X post (under 280 characters) with relevant hashtags
                2. A LinkedIn post (more professional, 2-3 sentences)
                3. A Facebook post (engaging, with a call to action)
                
                Social Media Posts:
                """
            )
            
            social_chain = LLMChain(
                llm=self.llm,
                prompt=social_prompt,
                output_key="social_posts",
                verbose=True
            )
            
            # Combine into sequential chain
            self.pipeline = SequentialChain(
                chains=[blog_chain, summary_chain, keywords_chain, social_chain],
                input_variables=["topic", "tone", "length"],
                output_variables=["blog_post", "summary", "keywords", "social_posts"],
                verbose=True
            )
            
        except Exception as e:
            st.error(f"Failed to setup pipeline: {format_error_message(e)}")
    
    def run_pipeline(self, topic: str, tone: str, length: str) -> dict:
        """Run the content generation pipeline."""
        if not self.pipeline:
            return {"error": "Pipeline not initialized"}
        
        try:
            result = self.pipeline({
                "topic": topic,
                "tone": tone,
                "length": length
            })
            return result
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            return {"error": format_error_message(e)}


# Main content
st.markdown("## 🔗 Content Generation Workflow")

st.info("""
**Content Generation Workflow:** This pipeline chains multiple LLM operations to create a complete content marketing package.

**Flow:** Topic + Parameters → Blog Post → Summary → SEO Keywords → Social Media Posts
""")

# Pipeline configuration section
st.markdown("### 📝 Content Configuration")

col1, col2, col3 = st.columns(3)

with col1:
    topic = st.text_input(
        "Content Topic",
        placeholder="e.g., Artificial Intelligence in Healthcare",
        help="The main topic for your content"
    )

with col2:
    tone = st.selectbox(
        "Writing Tone",
        options=["professional", "casual", "informative", "persuasive", "technical", "friendly"],
        index=0,
        help="The tone and style of writing"
    )

with col3:
    length = st.selectbox(
        "Blog Post Length",
        options=["short (300-500 words)", "medium (500-800 words)", "long (800+ words)"],
        index=1,
        help="Desired length of the blog post"
    )


# Run pipeline
if st.button("🚀 Generate Content Pipeline", type="primary", disabled=not topic.strip()):
    if not topic.strip():
        st.warning("Please enter a topic to generate content.")
    else:
        with st.spinner("Running content generation pipeline..."):
            # Initialize pipeline
            pipeline = ContentPipeline()
            
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔄 Initializing pipeline...")
            progress_bar.progress(10)
            
            # Run the pipeline
            result = pipeline.run_pipeline(topic, tone, length)
            
            if "error" in result:
                st.error(f"Pipeline failed: {result['error']}")
            else:
                # Show results
                progress_bar.progress(100)
                status_text.text("✅ Pipeline completed successfully!")
                
                st.markdown("## 📊 Generated Content")
                
                # Blog Post
                with st.expander("📝 Blog Post", expanded=True):
                    st.markdown(result.get("blog_post", "No content generated"))
                
                # Summary
                with st.expander("📄 Summary"):
                    st.markdown(result.get("summary", "No summary generated"))
                
                # Keywords
                with st.expander("🔍 SEO Keywords"):
                    keywords = result.get("keywords", "No keywords generated")
                    st.markdown(f"**Keywords:** {keywords}")
                    
                    # Display as tags
                    if keywords and keywords != "No keywords generated":
                        keyword_list = [k.strip() for k in keywords.split(",")]
                        tag_html = " ".join([f'<span style="background-color: #e1f5fe; padding: 2px 6px; border-radius: 3px; margin: 2px; display: inline-block;">{k}</span>' for k in keyword_list])
                        st.markdown(tag_html, unsafe_allow_html=True)
                
                # Social Media Posts
                with st.expander("📱 Social Media Posts"):
                    social_content = result.get("social_posts", "No social posts generated")
                    st.markdown(social_content)
                
                # Download option
                st.markdown("### 💾 Export Content")
                
                # Combine all content for download
                full_content = f"""
# Content Package: {topic}

## Blog Post
{result.get('blog_post', '')}

## Summary
{result.get('summary', '')}

## SEO Keywords
{result.get('keywords', '')}

## Social Media Posts
{result.get('social_posts', '')}

---
Generated by LangChain Sequential Chain Pipeline
                """
                
                st.download_button(
                    label="📥 Download Content Package",
                    data=full_content,
                    file_name=f"content_package_{topic.replace(' ', '_').lower()}.md",
                    mime="text/markdown"
                )

# Learning section
st.markdown("---")
st.markdown("## 🎓 How Sequential Chains Work")

with st.expander("🔍 Learn More About Sequential Chains"):
    st.markdown("""
    **Sequential Chains** allow you to connect multiple LLM operations where:
    
    1. **Each chain has a specific purpose** (blog writing, summarizing, keyword extraction)
    2. **Outputs become inputs** for the next chain in the sequence
    3. **Complex workflows** can be built from simple components
    4. **Reusable patterns** can be created for different content types
    
    **Key Benefits:**
    - **Modularity**: Each step is independent and reusable
    - **Flexibility**: Easy to modify or reorder steps
    - **Quality**: Specialized prompts for each task
    - **Efficiency**: Automated multi-step workflows
    
    **Use Cases:**
    - Content marketing pipelines
    - Document analysis workflows
    - Creative writing assistance
    - Data processing chains
    """)

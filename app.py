import streamlit as st
import pandas as pd
import time
import re
import random
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Set page configuration
st.set_page_config(
    page_title="Frontend Quiz web app ",
    page_icon="❓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        padding: 20px;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4527A0, #7B1FA2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
        margin-top: 220;  
    }
    
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #5E35B1;
        margin-bottom: 1.5rem;
        position: relative;
        padding-left: 15px;
    }
    
    .sub-header:before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 5px;
        border-radius: 5px;
    }
    
    /* Topic Cards */
    .topic-card {
        background: white;
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 1px solid #E0E0E0;
        margin-bottom: 25px;
    }
    
    .topic-card:hover {
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        border-color: #B39DDB;
        background-color: #F9F7FE;
    }
    
    .topic-icon {
        font-size: 3.5rem;
        margin-bottom: 15px;
        background: #EDE7F6;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        margin: 0 auto 20px auto;
    }
    
    .topic-card h3 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 10px;
        color: #4527A0;
    }
    
    .topic-card p {
        color: #757575;
        font-size: 0.95rem;
    }
    
    /* Result Cards */
    .result-card {
        background-color: white;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease;
        border-left-width: 5px; /* Initial border width */
    }
    
    .result-card:hover {
        border-left-width: 8px;
        background-color: #F9F7FE;
    }
    
    .result-card h3 {
        color: #4527A0;
        margin-bottom: 15px;
        font-weight: 600;
    }
    
    /* Answer Styles */
    .correct-answer {
        color: #2E7D32;
        font-weight: 600;
        position: relative;
        padding-left: 25px;
    }
    
    .correct-answer:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #2E7D32;
        font-weight: bold;
    }
    
    .wrong-answer {
        color: #C62828;
        text-decoration: line-through;
        position: relative;
        padding-left: 25px;
    }
    
    .wrong-answer:before {
        content: "✗";
        position: absolute;
        left: 0;
        color: #C62828;
        font-weight: bold;
    }
    
    /* Timer */
    .timer {
       font-size: small;
    font-weight: 500;
    color: #4527A0;
    text-align: center;
    margin-bottom: 10px;
    background: white;
    padding: 10px 20px;
    border-radius: 50px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    display: inline-block;
    }
    
    .timer-container {
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Form Styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #E0E0E0;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #7B1FA2;
        box-shadow: 0 0 0 3px rgba(123, 31, 162, 0.15);
        outline: none;
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: 500;
        transition: all 0.3s ease;
        border: none;
        background-color: #5E35B1;
        color: white;
        margin-top: 15px;
    }
    
    .stButton > button:hover {
        background-color: #4527A0;
        box-shadow: 0 5px 15px rgba(94, 53, 177, 0.3);
    }
    
    /* Radio Button Styling */
    .stRadio > div {
        border-radius: 16px;
        padding: 5px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }
    
    .stRadio > div > div > label:hover {
        background-color: #F5F0FF;
        border-radius: 8px;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background-color: #7B1FA2;
    }
    
    /* Download Buttons */
    .download-button {
        display: inline-block;
        padding: 12px 24px;
        color: white;
        text-decoration: none;
        border-radius: 10px;
        font-weight: 500;
        margin: 10px 0;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        text-align: center;
        background-color: #5E35B1;
        color: white;
    }
    
    .download-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(94, 53, 177, 0.4);
    }
    
    /* Question Styling */
    .question-container {
        background: white;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }
    
    .question-number {
        font-size: 1rem;
        color: #7B1FA2;
        font-weight: 500;
        margin-bottom: 10px;
    }
    
    .question-text {
        font-size: 1.4rem;
        font-weight: 600;
        color: #212121;
        margin-bottom: 25px;
        line-height: 1.5;
    }
    
    /* Option Cards */
    .option-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-top: 25px;
    }
    
    .option-card {
        background: #F5F5F5;
        border: 2px solid #E0E0E0;
        border-radius: 12px;
        padding: 15px;
        cursor: pointer;
        transition: all 0.2s ease;
        color: #212121;
    }
    
    .option-card:hover {
        border-color: #B39DDB;
        background: #EDE7F6;
        
    }
    
    .option-card.selected {
        border-color: #5E35B1;
        background: #EDE7F6;
    }
    
    /* Summary Card */
    .summary-card {
        color: white;
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(94, 53, 177, 0.3);
    }
    
    .summary-card h3 {
        font-size: 1.8rem;
        margin-bottom: 20px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
        padding-bottom: 10px;
    }
    
    .summary-card p {
        font-size: 1.1rem;
        margin-bottom: 10px;
    }
    
    .score-highlight {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 20px 0;
        text-align: center;
    }
    
    /* Animation for correct/wrong answers */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 1s infinite;
    }
    
    /* Confetti effect for high scores */
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background-color: #f2d74e;
        opacity: 0;
        animation: confetti 5s ease-in-out infinite;
    }
    
    @keyframes confetti {
        0% { transform: translateY(0); opacity: 1; }
        100% { transform: translateY(100vh); opacity: 0; }
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .sub-header {
            font-size: 1.5rem;
        }
        
        .topic-icon {
            font-size: 2.5rem;
            width: 60px;
            height: 60px;
        }
        
        .question-text {
            font-size: 1.2rem;
        }
        
        .summary-card {
            padding: 20px;
        }
        
        .score-highlight {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_info' not in st.session_state:
    st.session_state.user_info = {'name': '', 'phone': '', 'age': ''}
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'end_time' not in st.session_state:
    st.session_state.end_time = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False
if 'selected_options' not in st.session_state:
    st.session_state.selected_options = {}

# Quiz questions database
quiz_questions = {
    'nextjs': {
        'medium': [
            {
                'question': 'What is the main advantage of Next.js over plain React?',
                'options': [
                    'Server-side rendering capabilities',
                    'Better state management',
                    'More UI components',
                    'Faster development time'
                ],
                'correct': 'Server-side rendering capabilities'
            },
            {
                'question': 'Which function is used to fetch data at build time in Next.js?',
                'options': [
                    'getServerSideProps',
                    'getStaticProps',
                    'getInitialProps',
                    'fetchData'
                ],
                'correct': 'getStaticProps'
            },
            {
                'question': 'What is the purpose of the _app.js file in Next.js?',
                'options': [
                    'To initialize page props',
                    'To persist layout between page changes',
                    'To create API routes',
                    'To configure webpack'
                ],
                'correct': 'To persist layout between page changes'
            },
            {
                'question': 'How do you create dynamic routes in Next.js?',
                'options': [
                    'Using the [param].js file naming convention',
                    'Using the Route component',
                    'Using the Link component with dynamic props',
                    'Using the useRouter hook'
                ],
                'correct': 'Using the [param].js file naming convention'
            },
            {
                'question': 'What is Next.js API routes used for?',
                'options': [
                    'Creating server-side rendered pages',
                    'Creating backend API endpoints',
                    'Connecting to external APIs',
                    'Managing state in the application'
                ],
                'correct': 'Creating backend API endpoints'
            },
            {
                'question': 'Which Next.js feature allows you to split your application into smaller chunks?',
                'options': [
                    'Code Splitting',
                    'Dynamic Imports',
                    'Lazy Loading',
                    'All of the above'
                ],
                'correct': 'All of the above'
            },
            {
                'question': 'What is the purpose of the next.config.js file?',
                'options': [
                    'To configure the Next.js application',
                    'To define environment variables',
                    'To create API routes',
                    'To define page components'
                ],
                'correct': 'To configure the Next.js application'
            },
            {
                'question': 'Which of the following is NOT a Next.js data fetching method?',
                'options': [
                    'getStaticProps',
                    'getServerSideProps',
                    'getStaticPaths',
                    'getClientSideProps'
                ],
                'correct': 'getClientSideProps'
            },
            {
                'question': 'What is the purpose of the Link component in Next.js?',
                'options': [
                    'To create hyperlinks to external websites',
                    'To enable client-side navigation between pages',
                    'To link CSS files to components',
                    'To connect to backend APIs'
                ],
                'correct': 'To enable client-side navigation between pages'
            },
            {
                'question': 'How can you add global CSS in a Next.js application?',
                'options': [
                    'Import it in the _app.js file',
                    'Import it in every component that needs it',
                    'Add it to the public folder',
                    'Use inline styles only'
                ],
                'correct': 'Import it in the _app.js file'
            }
        ],
        'hard': [
            {
                'question': 'What is the purpose of Incremental Static Regeneration in Next.js?',
                'options': [
                    'To update static pages after deployment without rebuilding the entire site',
                    'To incrementally add new static pages to an existing site',
                    'To regenerate dynamic routes on each request',
                    'To improve the build time of large applications'
                ],
                'correct': 'To update static pages after deployment without rebuilding the entire site'
            },
            {
                'question': 'Which lifecycle method is specific to Next.js and not found in React?',
                'options': [
                    'componentDidMount',
                    'getInitialProps',
                    'shouldComponentUpdate',
                    'componentWillUnmount'
                ],
                'correct': 'getInitialProps'
            },
            {
                'question': 'What is the correct way to access query parameters in a Next.js page component?',
                'options': [
                    'Using the useRouter hook from next/router',
                    'Using the window.location object',
                    'Using the this.props.query object',
                    'Using the useQuery hook from React Query'
                ],
                'correct': 'Using the useRouter hook from next/router'
            },
            {
                'question': 'What is the purpose of the fallback property in getStaticPaths?',
                'options': [
                    'To specify a fallback page for 404 errors',
                    'To control whether paths not returned by getStaticPaths should be generated at build time or on-demand',
                    'To provide a fallback UI while data is loading',
                    'To redirect users to a different page when a path is not found'
                ],
                'correct': 'To control whether paths not returned by getStaticPaths should be generated at build time or on-demand'
            },
            {
                'question': 'Which of the following is NOT a valid Next.js optimization technique?',
                'options': [
                    'Image Optimization with next/image',
                    'Automatic Static Optimization',
                    'Server Components',
                    'Virtual DOM Caching'
                ],
                'correct': 'Virtual DOM Caching'
            },
            {
                'question': 'What is the purpose of the _middleware.js file in Next.js 12+?',
                'options': [
                    'To run code before a request is completed',
                    'To handle API requests',
                    'To configure the application',
                    'To define global components'
                ],
                'correct': 'To run code before a request is completed'
            },
            {
                'question': 'How can you implement internationalization in Next.js?',
                'options': [
                    'Using the built-in i18n routing support',
                    'Using the Intl JavaScript API',
                    'Using external libraries like react-intl',
                    'All of the above'
                ],
                'correct': 'All of the above'
            },
            {
                'question': 'What is the purpose of the revalidate property in getStaticProps?',
                'options': [
                    'To validate user input',
                    'To specify how often a page should be regenerated',
                    'To check if the data is still valid',
                    'To validate API responses'
                ],
                'correct': 'To specify how often a page should be regenerated'
            },
            {
                'question': 'Which of the following is true about the App Router in Next.js 13+?',
                'options': [
                    'It uses file-system based routing with app/ directory',
                    'It supports React Server Components',
                    'It introduces new data fetching methods',
                    'All of the above'
                ],
                'correct': 'All of the above'
            },
            {
                'question': 'What is the purpose of the next/script component?',
                'options': [
                    'To optimize loading of third-party scripts',
                    'To write server-side JavaScript',
                    'To create client-side routing',
                    'To define API routes'
                ],
                'correct': 'To optimize loading of third-party scripts'
            }
        ]
    },
    'html': {
        'medium': [
            {
                'question': 'What does HTML stand for?',
                'options': [
                    'Hyper Text Markup Language',
                    'High Tech Modern Language',
                    'Hyper Transfer Markup Language',
                    'Hyper Text Modern Links'
                ],
                'correct': 'Hyper Text Markup Language'
            },
            {
                'question': 'Which HTML element is used to define the title of a document?',
                'options': [
                    '<head>',
                    '<title>',
                    '<header>',
                    '<top>'
                ],
                'correct': '<title>'
            },
            {
                'question': 'Which HTML attribute is used to define inline styles?',
                'options': [
                    'class',
                    'style',
                    'font',
                    'styles'
                ],
                'correct': 'style'
            },
            {
                'question': 'Which HTML element is used to create a form?',
                'options': [
                    '<input>',
                    '<form>',
                    '<section>',
                    '<formfield>'
                ],
                'correct': '<form>'
            },
            {
                'question': 'What is the correct HTML element for inserting a line break?',
                'options': [
                    '<lb>',
                    '<break>',
                    '<br>',
                    '<newline>'
                ],
                'correct': '<br>'
            },
            {
                'question': 'Which HTML element is used to define an unordered list?',
                'options': [
                    '<ul>',
                    '<ol>',
                    '<li>',
                    '<list>'
                ],
                'correct': '<ul>'
            },
            {
                'question': 'What is the correct HTML for creating a hyperlink?',
                'options': [
                    '<a url="http://example.com">Example</a>',
                    '<a href="http://example.com">Example</a>',
                    '<hyperlink href="http://example.com">Example</hyperlink>',
                    '<link to="http://example.com">Example</link>'
                ],
                'correct': '<a href="http://example.com">Example</a>'
            },
            {
                'question': 'Which HTML element defines the main content of a document?',
                'options': [
                    '<section>',
                    '<content>',
                    '<main>',
                    '<body>'
                ],
                'correct': '<main>'
            },
            {
                'question': 'Which HTML element is used to specify a footer for a document or section?',
                'options': [
                    '<bottom>',
                    '<footer>',
                    '<end>',
                    '<section>'
                ],
                'correct': '<footer>'
            },
            {
                'question': 'What is the purpose of the alt attribute in the <img> tag?',
                'options': [
                    'To define alternative text for an image',
                    'To specify the alignment of the image',
                    'To provide a title for the image',
                    'To set the width and height of the image'
                ],
                'correct': 'To define alternative text for an image'
            }
        ],
        'hard': [
            {
                'question': 'Which HTML5 element is used for specifying a footer for a section or page?',
                'options': [
                    '<footer>',
                    '<section>',
                    '<bottom>',
                    '<div class="footer">'
                ],
                'correct': '<footer>'
            },
            {
                'question': 'What is the purpose of the <canvas> element in HTML5?',
                'options': [
                    'To draw graphics via JavaScript',
                    'To create a container for external content',
                    'To display database data in a table format',
                    'To create a scrollable container'
                ],
                'correct': 'To draw graphics via JavaScript'
            },
            {
                'question': 'Which of the following is NOT a valid HTML5 semantic element?',
                'options': [
                    '<article>',
                    '<aside>',
                    '<dialog>',
                    '<container>'
                ],
                'correct': '<container>'
            },
            {
                'question': 'What is the purpose of the srcset attribute in the <img> tag?',
                'options': [
                    'To specify multiple image sources for different screen sizes',
                    'To set the source of the image',
                    'To provide alternative text for an image',
                    'To specify the dimensions of the image'
                ],
                'correct': 'To specify multiple image sources for different screen sizes'
            },
            {
                'question': 'Which attribute is used to specify that an input field must be filled out?',
                'options': [
                    'required',
                    'validate',
                    'placeholder',
                    'important'
                ],
                'correct': 'required'
            },
            {
                'question': 'What is the purpose of the <datalist> element?',
                'options': [
                    'To specify a list of pre-defined options for an input element',
                    'To create a dropdown list',
                    'To store data in the browser',
                    'To create a data table'
                ],
                'correct': 'To specify a list of pre-defined options for an input element'
            },
            {
                'question': 'Which HTML5 input type is used for picking a date and time?',
                'options': [
                    '<input type="date">',
                    '<input type="time">',
                    '<input type="datetime-local">',
                    '<input type="calendar">'
                ],
                'correct': '<input type="datetime-local">'
            },
            {
                'question': 'What is the purpose of the defer attribute in the <script> tag?',
                'options': [
                    'To defer the execution of the script until the page has finished parsing',
                    'To prevent the script from executing',
                    'To load the script asynchronously',
                    'To specify that the script is from an external source'
                ],
                'correct': 'To defer the execution of the script until the page has finished parsing'
            },
            {
                'question': 'Which HTML5 API is used for drag and drop functionality?',
                'options': [
                    'Drag and Drop API',
                    'Gesture API',
                    'Touch API',
                    'Mouse Events API'
                ],
                'correct': 'Drag and Drop API'
            },
            {
                'question': 'What is the purpose of the <figure> and <figcaption> elements?',
                'options': [
                    'To define a container for images with captions',
                    'To create a figure or chart with JavaScript',
                    'To embed external content like videos',
                    'To create a floating element on the page'
                ],
                'correct': 'To define a container for images with captions'
            }
        ]
    },
    'css': {
        'medium': [
            {
                'question': 'What does CSS stand for?',
                'options': [
                    'Cascading Style Sheets',
                    'Creative Style Sheets',
                    'Computer Style Sheets',
                    'Colorful Style Sheets'
                ],
                'correct': 'Cascading Style Sheets'
            },
            {
                'question': 'Which CSS property is used to change the text color of an element?',
                'options': [
                    'text-color',
                    'color',
                    'font-color',
                    'text-style'
                ],
                'correct': 'color'
            },
            {
                'question': 'Which CSS property controls the text size?',
                'options': [
                    'text-size',
                    'font-style',
                    'font-size',
                    'text-style'
                ],
                'correct': 'font-size'
            },
            {
                'question': 'How do you select an element with id "demo"?',
                'options': [
                    '.demo',
                    '#demo',
                    'demo',
                    '*demo'
                ],
                'correct': '#demo'
            },
            {
                'question': 'How do you select elements with class name "test"?',
                'options': [
                    '.test',
                    '#test',
                    'test',
                    '*test'
                ],
                'correct': '.test'
            },
            {
                'question': 'What is the default value of the position property?',
                'options': [
                    'relative',
                    'fixed',
                    'absolute',
                    'static'
                ],
                'correct': 'static'
            },
            {
                'question': 'Which property is used to change the background color?',
                'options': [
                    'bgcolor',
                    'background-color',
                    'color',
                    'background'
                ],
                'correct': 'background-color'
            },
            {
                'question': 'How do you make each word in a text start with a capital letter?',
                'options': [
                    'text-transform: capitalize',
                    'text-transform: uppercase',
                    'text-style: capital',
                    'font-transform: capitalize'
                ],
                'correct': 'text-transform: capitalize'
            },
            {
                'question': 'Which property is used to change the font of an element?',
                'options': [
                    'font-style',
                    'font-family',
                    'font-weight',
                    'font-size'
                ],
                'correct': 'font-family'
            },
            {
                'question': 'How do you display a border like this: "Solid red border"?',
                'options': [
                    'border: solid red',
                    'border-color: red; border-style: solid',
                    'border-color: red; border-type: solid',
                    'border: red solid'
                ],
                'correct': 'border: solid red'
            }
        ],
        'hard': [
            {
                'question': 'What is the purpose of the z-index property in CSS?',
                'options': [
                    'To count the number of elements',
                    'To set the horizontal position',
                    'To set the stack order of elements',
                    'To set the zoom level of an element'
                ],
                'correct': 'To set the stack order of elements'
            },
            {
                'question': 'Which CSS property is used to create a grid layout?',
                'options': [
                    'grid-template',
                    'display: grid',
                    'grid-layout',
                    'display: grid-layout'
                ],
                'correct': 'display: grid'
            },
            {
                'question': 'What is the purpose of the CSS property "flex-grow"?',
                'options': [
                    'To specify how much a flex item will grow relative to the rest of the flex items',
                    'To make an element grow in size when hovered',
                    'To specify the direction in which the flex container grows',
                    'To specify the growth factor of the flex container'
                ],
                'correct': 'To specify how much a flex item will grow relative to the rest of the flex items'
            },
            {
                'question': 'Which CSS function is used to create a smooth transition between two or more colors?',
                'options': [
                    'transition()',
                    'smooth()',
                    'gradient()',
                    'linear-gradient()'
                ],
                'correct': 'linear-gradient()'
            },
            {
                'question': 'What is the purpose of the CSS "calc()" function?',
                'options': [
                    'To calculate the sum of two numbers',
                    'To perform calculations for CSS property values',
                    'To calculate the dimensions of an element',
                    'To calculate the position of an element'
                ],
                'correct': 'To perform calculations for CSS property values'
            },
            {
                'question': 'Which CSS property is used to create animations?',
                'options': [
                    'animation',
                    'transition',
                    'transform',
                    'motion'
                ],
                'correct': 'animation'
            },
            {
                'question': 'What is the purpose of the CSS "clip-path" property?',
                'options': [
                    'To hide overflow content',
                    'To create a clipping region that sets what part of an element should be shown',
                    'To clip images to a specific size',
                    'To create a path for animations'
                ],
                'correct': 'To create a clipping region that sets what part of an element should be shown'
            },
            {
                'question': 'Which CSS selector selects all elements with a specific attribute?',
                'options': [
                    '[attribute]',
                    '.attribute',
                    '#attribute',
                    '*attribute'
                ],
                'correct': '[attribute]'
            },
            {
                'question': 'What is the purpose of the CSS "counter-increment" property?',
                'options': [
                    'To create a counter for numbered lists',
                    'To increment the value of a variable',
                    'To count the number of elements',
                    'To increase the size of an element'
                ],
                'correct': 'To create a counter for numbered lists'
            },
            {
                'question': 'Which CSS property is used to specify the space between characters?',
                'options': [
                    'character-spacing',
                    'letter-spacing',
                    'text-spacing',
                    'word-spacing'
                ],
                'correct': 'letter-spacing'
            }
        ]
    },
    'javascript': {
        'medium': [
            {
                'question': 'Which operator is used to assign a value to a variable?',
                'options': [
                    '=',
                    '*',
                    '-',
                    'x'
                ],
                'correct': '='
            },
            {
                'question': 'What will the following code return: Boolean(10 > 9)',
                'options': [
                    'true',
                    'false',
                    'NaN',
                    'undefined'
                ],
                'correct': 'true'
            },
            {
                'question': 'How do you declare a JavaScript variable?',
                'options': [
                    'var carName',
                    'variable carName',
                    'v carName',
                    'let carName'
                ],
                'correct': 'var carName'
            },
            {
                'question': 'Which event occurs when the user clicks on an HTML element?',
                'options': [
                    'onmouseover',
                    'onchange',
                    'onclick',
                    'onmouseclick'
                ],
                'correct': 'onclick'
            },
            {
                'question': 'How do you create a function in JavaScript?',
                'options': [
                    'function myFunction()',
                    'function:myFunction()',
                    'function = myFunction()',
                    'function => myFunction()'
                ],
                'correct': 'function myFunction()'
            },
            {
                'question': 'How do you call a function named "myFunction"?',
                'options': [
                    'call myFunction()',
                    'myFunction()',
                    'call function myFunction()',
                    'execute myFunction()'
                ],
                'correct': 'myFunction()'
            },
            {
                'question': 'How to write an IF statement in JavaScript?',
                'options': [
                    'if i = 5 then',
                    'if i == 5 then',
                    'if (i == 5)',
                    'if i = 5'
                ],
                'correct': 'if (i == 5)'
            },
            {
                'question': 'How to write an IF statement for executing some code if "i" is NOT equal to 5?',
                'options': [
                    'if (i != 5)',
                    'if i <> 5',
                    'if (i <> 5)',
                    'if i =! 5 then'
                ],
                'correct': 'if (i != 5)'
            },
            {
                'question': 'How does a WHILE loop start?',
                'options': [
                    'while (i <= 10)',
                    'while i = 1 to 10',
                    'while (i <= 10; i++)',
                    'while i <= 10'
                ],
                'correct': 'while (i <= 10)'
            },
            {
                'question': 'How does a FOR loop start?',
                'options': [
                    'for (i = 0; i <= 5; i++)',
                    'for (i <= 5; i++)',
                    'for i = 1 to 5',
                    'for (i = 0; i <= 5)'
                ],
                'correct': 'for (i = 0; i <= 5; i++)'
            }
        ],
        'hard': [
            {
                'question': 'What is a closure in JavaScript?',
                'options': [
                    'A function that has access to variables in its outer lexical environment',
                    'A way to close a browser window using JavaScript',
                    'A method to terminate a loop',
                    'A data structure for storing key-value pairs'
                ],
                'correct': 'A function that has access to variables in its outer lexical environment'
            },
            {
                'question': 'What is the purpose of the "use strict" directive?',
                'options': [
                    'To enforce stricter parsing and error handling in JavaScript',
                    'To make the code execute faster',
                    'To enable new JavaScript features',
                    'To connect to a strict server mode'
                ],
                'correct': 'To enforce stricter parsing and error handling in JavaScript'
            },
            {
                'question': 'What is the difference between "==" and "===" operators?',
                'options': [
                    '"==" compares values, "===" compares values and types',
                    '"==" compares types, "===" compares values',
                    'They are identical in functionality',
                    '"==" is used for assignment, "===" is used for comparison'
                ],
                'correct': '"==" compares values, "===" compares values and types'
            },
            {
                'question': 'What is the purpose of the "Promise" object?',
                'options': [
                    'To represent a value that may be available now, in the future, or never',
                    'To promise the user that the code will work',
                    'To ensure variables are properly declared',
                    'To lock variables from being modified'
                ],
                'correct': 'To represent a value that may be available now, in the future, or never'
            },
            {
                'question': 'What is event bubbling in JavaScript?',
                'options': [
                    'The process where an event triggers on the deepest target element, then propagates upward',
                    'A method to create multiple events at once',
                    'A way to prevent events from triggering',
                    'The process of validating events before execution'
                ],
                'correct': 'The process where an event triggers on the deepest target element, then propagates upward'
            },
            {
                'question': 'What is the purpose of the "map" method in JavaScript arrays?',
                'options': [
                    'To create a new array with the results of calling a function on every element',
                    'To map one array to another array',
                    'To search for an element in an array',
                    'To sort the elements of an array'
                ],
                'correct': 'To create a new array with the results of calling a function on every element'
            },
            {
                'question': 'What is a generator function in JavaScript?',
                'options': [
                    'A function that can be paused and resumed, yielding multiple values',
                    'A function that generates other functions',
                    'A function that creates objects automatically',
                    'A built-in function to generate random numbers'
                ],
                'correct': 'A function that can be paused and resumed, yielding multiple values'
            },
            {
                'question': 'What is the purpose of the "reduce" method in JavaScript arrays?',
                'options': [
                    'To execute a reducer function on each element, resulting in a single output value',
                    'To reduce the size of the array',
                    'To remove duplicate elements from an array',
                    'To reduce the memory usage of an array'
                ],
                'correct': 'To execute a reducer function on each element, resulting in a single output value'
            },
            {
                'question': 'What is the purpose of the "async/await" syntax?',
                'options': [
                    'To simplify asynchronous code and make it look more like synchronous code',
                    'To make code execute faster',
                    'To prevent race conditions',
                    'To create multi-threaded JavaScript applications'
                ],
                'correct': 'To simplify asynchronous code and make it look more like synchronous code'
            },
            {
                'question': 'What is the JavaScript "prototype" property used for?',
                'options': [
                    'To add properties and methods to object constructors',
                    'To protect objects from being modified',
                    'To create private variables in objects',
                    'To define the initial state of an object'
                ],
                'correct': 'To add properties and methods to object constructors'
            }
        ]
    }
}

# Helper functions
def validate_phone(phone):
    """Validate phone number format."""
    pattern = r'^\d{10}$'
    if re.match(pattern, phone):
        return True
    return False

def validate_age(age):
    """Validate age is a number between 10 and 100."""
    try:
        age_num = int(age)
        if 10 <= age_num <= 100:
            return True
        return False
    except ValueError:
        return False

def generate_quiz(topic, difficulty, num_questions=10):
    """Generate a quiz with specified topic and difficulty."""
    if topic in quiz_questions and difficulty in quiz_questions[topic]:
        questions = quiz_questions[topic][difficulty]
        if len(questions) > num_questions:
            return random.sample(questions, num_questions)
        return questions
    return []

def calculate_score(answers, quiz_data):
    """Calculate the score based on answers and quiz data."""
    score = 0
    for i, question in enumerate(quiz_data):
        if i in answers and answers[i] == question['correct']:
            score += 1
    return score

def get_excel_download_link(user_info, quiz_data, answers, score, time_taken):
    """Generate a download link for Excel results."""
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # Create a DataFrame for user info
    user_df = pd.DataFrame({
        'Name': [user_info['name']],
        'Phone': [user_info['phone']],
        'Age': [user_info['age']],
        'Score': [f"{score}/{len(quiz_data)}"],
        'Percentage': [f"{(score/len(quiz_data))*100:.2f}%"],
        'Time Taken': [f"{time_taken:.2f} seconds"]
    })
    
    # Create a DataFrame for quiz results
    results = []
    for i, question in enumerate(quiz_data):
        user_answer = answers.get(i, "Not answered")
        correct_answer = question['correct']
        is_correct = user_answer == correct_answer
        
        results.append({
            'Question': question['question'],
            'Your Answer': user_answer,
            'Correct Answer': correct_answer,
            'Result': "Correct" if is_correct else "Incorrect"
        })
    
    results_df = pd.DataFrame(results)
    
    # Write DataFrames to Excel
    user_df.to_excel(writer, sheet_name='Summary', index=False)
    results_df.to_excel(writer, sheet_name='Quiz Results', index=False)
    
    # Save the Excel file
    writer.close()
    
    # Create download link
    b64 = base64.b64encode(output.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{user_info["name"]}_quiz_results.xlsx" class="download-button">Download Excel Results</a>'
    return href

def get_pdf_download_link(user_info, quiz_data, answers, score, time_taken):
    """Generate a download link for PDF results."""
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Add title
    title = Paragraph(f"Quiz Results for {user_info['name']}", styles['Title'])
    elements.append(title)
    
    # Add user info
    elements.append(Paragraph(f"Phone: {user_info['phone']}", styles['Normal']))
    elements.append(Paragraph(f"Age: {user_info['age']}", styles['Normal']))
    elements.append(Paragraph(f"Score: {score}/{len(quiz_data)} ({(score/len(quiz_data))*100:.2f}%)", styles['Normal']))
    elements.append(Paragraph(f"Time Taken: {time_taken:.2f} seconds", styles['Normal']))
    
    # Add quiz results
    elements.append(Paragraph("Quiz Results", styles['Heading2']))
    
    # Create table data
    table_data = [["Question", "Your Answer", "Correct Answer", "Result"]]
    
    for i, question in enumerate(quiz_data):
        user_answer = answers.get(i, "Not answered")
        correct_answer = question['correct']
        is_correct = user_answer == correct_answer
        
        table_data.append([
            question['question'],
            user_answer,
            correct_answer,
            "Correct" if is_correct else "Incorrect"
        ])
    
    # Create table
    table = Table(table_data)
    
    # Add style to table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    
    # Add conditional formatting for correct/incorrect answers
    for i in range(1, len(table_data)):
        if table_data[i][3] == "Correct":
            style.add('BACKGROUND', (3, i), (3, i), colors.lightgreen)
        else:
            style.add('BACKGROUND', (3, i), (3, i), colors.lightcoral)
    
    table.setStyle(style)
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    
    # Create download link
    b64 = base64.b64encode(buffer.getvalue()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{user_info["name"]}_quiz_results.pdf" class="download-button">Download PDF Results</a>'
    return href

def get_csv_download_link(user_info, quiz_data, answers, score, time_taken):
    """Generate a download link for CSV results."""
    # Create a DataFrame for quiz results
    results = []
    for i, question in enumerate(quiz_data):
        user_answer = answers.get(i, "Not answered")
        correct_answer = question['correct']
        is_correct = user_answer == correct_answer
        
        results.append({
            'Question': question['question'],
            'Your Answer': user_answer,
            'Correct Answer': correct_answer,
            'Result': "Correct" if is_correct else "Incorrect"
        })
    
    results_df = pd.DataFrame(results)
    
    # Add user info at the top
    user_info_df = pd.DataFrame({
        'Name': [user_info['name']],
        'Phone': [user_info['phone']],
        'Age': [user_info['age']],
        'Score': [f"{score}/{len(quiz_data)}"],
        'Percentage': [f"{(score/len(quiz_data))*100:.2f}%"],
        'Time Taken': [f"{time_taken:.2f} seconds"]
    })
    
    # Convert to CSV
    csv = user_info_df.to_csv(index=False) + "\n\n" + results_df.to_csv(index=False)
    
    # Create download link
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:text/csv;base64,{b64}" download="{user_info["name"]}_quiz_results.csv" class="download-button">Download CSV Results</a>'
    return href

def get_text_download_link(user_info, quiz_data, answers, score, time_taken):
    """Generate a download link for plain text results."""
    text = f"Quiz Results for {user_info['name']}\n"
    text += f"Phone: {user_info['phone']}\n"
    text += f"Age: {user_info['age']}\n"
    text += f"Score: {score}/{len(quiz_data)} ({(score/len(quiz_data))*100:.2f}%)\n"
    text += f"Time Taken: {time_taken:.2f} seconds\n\n"
    
    text += "Quiz Results:\n"
    for i, question in enumerate(quiz_data):
        user_answer = answers.get(i, "Not answered")
        correct_answer = question['correct']
        is_correct = user_answer == correct_answer
        
        text += f"Question {i+1}: {question['question']}\n"
        text += f"Your Answer: {user_answer}\n"
        text += f"Correct Answer: {correct_answer}\n"
        text += f"Result: {'Correct' if is_correct else 'Incorrect'}\n\n"
    
    # Create download link
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{user_info["name"]}_quiz_results.txt" class="download-button">Download Text Results</a>'
    return href

# Generate confetti effect for high scores
def generate_confetti():
    confetti_html = """
    <script>
    function createConfetti() {
        const confettiCount = 200;
        const container = document.body;
        
        for (let i = 0; i < confettiCount; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            
            // Random position
            confetti.style.left = Math.random() * 100 + 'vw';
            
            // Random size
            const size = Math.random() * 10 + 5;
            confetti.style.width = size + 'px';
            confetti.style.height = size + 'px';
            
            // Random color
            const colors = ['#f94144', '#f3722c', '#f8961e', '#f9c74f', '#90be6d', '#43aa8b', '#577590', '#7209b7'];
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            
            // Random rotation
            confetti.style.transform = `rotate(${Math.random() * 360}deg)`;
            
            // Random animation duration
            confetti.style.animationDuration = (Math.random() * 3 + 2) + 's';
            
            // Random delay
            confetti.style.animationDelay = Math.random() * 5 + 's';
            
            container.appendChild(confetti);
            
            // Remove confetti after animation
            setTimeout(() => {
                confetti.remove();
            }, 8000);
        }
    }
    
    // Call the function
    createConfetti();
    </script>
    """
    return confetti_html

# Main application
def main():
    # Display header
    st.markdown('<h1 class="main-header">Frontend Quiz Web App</h1>', unsafe_allow_html=True)
    
    # Home page
    if st.session_state.page == 'home':
        # Welcome message
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <p style="font-size: 1.2rem; color: #555;">
                Welcome to the Frontend Quiz Generator! Test your knowledge on various web development topics.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h2 class="sub-header">Choose a Topic</h2>', unsafe_allow_html=True)
        
        # Create a grid of topic cards
        col1, col2 = st.columns(2)
        
        with col1:
            # Next.js card
            st.markdown(
                """
                <div class="topic-card" onclick="document.getElementById('nextjs-button').click()">
                    <div class="topic-icon">⚛️</div>
                    <h3>Next.js</h3>
                    <p>Test your knowledge of Next.js framework, server-side rendering, and routing</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            # Hidden button to handle the click
            if st.button("Start Quiz - Next.js", key="nextjs-button", help="Start a Next.js quiz"):
                st.session_state.topic = 'nextjs'
                st.session_state.page = 'difficulty'
                st.rerun()
            
            # HTML card
            st.markdown(
                """
                <div class="topic-card" onclick="document.getElementById('html-button').click()">
                    <div class="topic-icon">🌐</div>
                    <h3>HTML</h3>
                    <p>Test your knowledge of HTML markup, semantic elements, and accessibility</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            # Hidden button to handle the click
            if st.button("Start Quiz - HTML", key="html-button", help="Start an HTML quiz"):
                st.session_state.topic = 'html'
                st.session_state.page = 'difficulty'
                st.rerun()
        
        with col2:
            # CSS card
            st.markdown(
                """
                <div class="topic-card" onclick="document.getElementById('css-button').click()">
                    <div class="topic-icon">🎨</div>
                    <h3>CSS</h3>
                    <p>Test your knowledge of CSS styling, layouts, animations, and responsive design</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            # Hidden button to handle the click
            if st.button("Start Quiz - CSS", key="css-button", help="Start a CSS quiz"):
                st.session_state.topic = 'css'
                st.session_state.page = 'difficulty'
                st.rerun()
            
            # JavaScript card
            st.markdown(
                """
                <div class="topic-card" onclick="document.getElementById('javascript-button').click()">
                    <div class="topic-icon">📜</div>
                    <h3>JavaScript</h3>
                    <p>Test your knowledge of JavaScript programming, DOM manipulation, and modern ES6+ features</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            # Hidden button to handle the click
            if st.button("Start Quiz - JavaScript", key="javascript-button", help="Start a JavaScript quiz"):
                st.session_state.topic = 'javascript'
                st.session_state.page = 'difficulty'
                st.rerun()
        
        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #E0E0E0;">
            <p style="color: #757575; font-size: 0.9rem;">
                © 2023 Frontend Quiz Generator | Created with Streamlit
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Difficulty selection page
    elif st.session_state.page == 'difficulty':
        st.markdown(f'<h2 class="sub-header">Select Difficulty for {st.session_state.topic.capitalize()} Quiz</h2>', unsafe_allow_html=True)
        
        # Description based on topic
        topic_descriptions = {
            'nextjs': "Next.js is a React framework that enables server-side rendering and static site generation.",
            'html': "HTML (HyperText Markup Language) is the standard markup language for documents designed to be displayed in a web browser.",
            'css': "CSS (Cascading Style Sheets) is a style sheet language used for describing the presentation of a document written in HTML.",
            'javascript': "JavaScript is a programming language that enables interactive web pages and is an essential part of web applications."
        }
        
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 16px; margin-bottom: 30px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);">
            <p style="color: #555;">{topic_descriptions.get(st.session_state.topic, "")}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(
                """
                <div class="topic-card" onclick="document.getElementById('medium-button').click()">
                    <div class="topic-icon">🔄</div>
                    <h3>Medium</h3>
                    <p>Standard difficulty level for intermediate developers</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            if st.button("Medium", key="medium-button"):
                st.session_state.difficulty = 'medium'
                st.session_state.page = 'user_info'
                st.rerun()
        
        with col2:
            st.markdown(
                """
                <div class="topic-card" onclick="document.getElementById('hard-button').click()">
                    <div class="topic-icon">🔥</div>
                    <h3>Hard</h3>
                    <p>Advanced difficulty level for experienced developers</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            if st.button("Hard", key="hard-button"):
                st.session_state.difficulty = 'hard'
                st.session_state.page = 'user_info'
                st.rerun()
        
        # Back button with improved styling
        st.markdown("""
        <div style="margin-top: 30px;">
        """, unsafe_allow_html=True)
        if st.button("← Back to Topics", key="back-to-topics"):
            st.session_state.page = 'home'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # User info page
    elif st.session_state.page == 'user_info':
        st.markdown(f'<h2 class="sub-header">Enter Your Information</h2>', unsafe_allow_html=True)
        
        # User info card
        st.markdown("""
        <div style="background: white;  border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);">
        """, unsafe_allow_html=True)
        
        with st.form("user_info_form"):
            st.markdown("<p style='color: #555; margin-bottom: 20px;'>Please provide your information to start the quiz.</p>", unsafe_allow_html=True)
            
            name = st.text_input("Full Name", value=st.session_state.user_info.get('name', ''))
            phone = st.text_input("Phone Number (10 digits without leading zero)", value=st.session_state.user_info.get('phone', ''))
            age = st.text_input("Age (10-100)", value=st.session_state.user_info.get('age', ''))
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Start Quiz")
            
            if submitted:
                error = False
                
                if not name:
                    st.error("Please enter your name.")
                    error = True
                
                if not validate_phone(phone):
                    st.error("Please enter a valid 10-digit phone number.")
                    error = True
                
                if not validate_age(age):
                    st.error("Please enter a valid age between 10 and 100.")
                    error = True
                
                if not error:
                    st.session_state.user_info = {
                        'name': name,
                        'phone': phone,
                        'age': age
                    }
                    
                    # Generate quiz
                    st.session_state.quiz_data = generate_quiz(
                        st.session_state.topic, 
                        st.session_state.difficulty
                    )
                    
                    # Reset quiz state
                    st.session_state.answers = {}
                    st.session_state.current_question = 0
                    st.session_state.start_time = time.time()
                    st.session_state.quiz_completed = False
                    
                    st.session_state.page = 'quiz'
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Back button
        st.markdown("""
        <div style="margin-top: 30px;">
        """, unsafe_allow_html=True)
        if st.button("← Back to Difficulty", key="back-to-difficulty"):
            st.session_state.page = 'difficulty'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Quiz page
    elif st.session_state.page == 'quiz':
        if not st.session_state.quiz_completed:
            # Display timer
            elapsed_time = time.time() - st.session_state.start_time
            st.markdown(f'<div class="timer-container"><div class="timer">⏱️ {elapsed_time:.1f} seconds</div></div>', unsafe_allow_html=True)
            
            # Display progress
            progress = (st.session_state.current_question + 1) / len(st.session_state.quiz_data)
            st.progress(progress)
            st.markdown(f"<p style='text-align: center; color: #555;'>Question {st.session_state.current_question + 1} of {len(st.session_state.quiz_data)}</p>", unsafe_allow_html=True)
            
            # Display current question
            current_q = st.session_state.quiz_data[st.session_state.current_question]
            
            st.markdown(f"""
            <div class="question-container">
                <div class="question-number">Question {st.session_state.current_question + 1}</div>
                <div class="question-text">{current_q['question']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display options with improved UI
            option_key = f"q{st.session_state.current_question}"
            selected_option = st.radio(
                "Select your answer:",
                current_q['options'],
                key=option_key,
                label_visibility="collapsed"
                
            )
            
            # Store the selected option
            st.session_state.selected_options[st.session_state.current_question] = selected_option
            
            # Navigation buttons
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("← Previous", disabled=st.session_state.current_question == 0):
                    # Save current answer
                    st.session_state.answers[st.session_state.current_question] = selected_option
                    # Go to previous question
                    st.session_state.current_question -= 1
                    st.rerun()
            
            with col2:
                if st.session_state.current_question < len(st.session_state.quiz_data) - 1:
                    next_button = st.button("Next →")
                    if next_button:
                        # Save current answer
                        st.session_state.answers[st.session_state.current_question] = selected_option
                        # Go to next question
                        st.session_state.current_question += 1
                        st.rerun()
                else:
                    finish_button = st.button("Finish Quiz")
                    if finish_button:
                        # Save current answer
                        st.session_state.answers[st.session_state.current_question] = selected_option
                        # Calculate score
                        st.session_state.score = calculate_score(st.session_state.answers, st.session_state.quiz_data)
                        # Record end time
                        st.session_state.end_time = time.time()
                        # Mark quiz as completed
                        st.session_state.quiz_completed = True
                        st.rerun()
        else:
            # Display results
            st.markdown('<h2 class="sub-header">Quiz Results</h2>', unsafe_allow_html=True)
            
            # Calculate time taken
            time_taken = st.session_state.end_time - st.session_state.start_time
            
            # Calculate percentage
            percentage = (st.session_state.score / len(st.session_state.quiz_data)) * 100
            
            # Display summary with improved UI
            st.markdown(f"""
            <div class="summary-card">
                <h3>Quiz Summary</h3>
                <p><strong>Name:</strong> {st.session_state.user_info['name']}</p>
                <p><strong>Topic:</strong> {st.session_state.topic.capitalize()}</p>
                <p><strong>Difficulty:</strong> {st.session_state.difficulty.capitalize()}</p>
                <div class="score-highlight">{st.session_state.score}/{len(st.session_state.quiz_data)} ({percentage:.2f}%)</div>
                <p><strong>Time taken:</strong> {time_taken:.2f} seconds</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add confetti for high scores
            if percentage >= 70:
                st.markdown(generate_confetti(), unsafe_allow_html=True)
            
            # Display detailed results
            st.markdown("<h3 class='sub-header'>Detailed Results</h3>", unsafe_allow_html=True)
            
            for i, question in enumerate(st.session_state.quiz_data):
                user_answer = st.session_state.answers.get(i, "Not answered")
                correct_answer = question['correct']
                is_correct = user_answer == correct_answer
                
                st.markdown(f"""
                <div class="result-card" style="border-left: 5px solid {'#4CAF50' if is_correct else '#F44336'}">
                    <p><strong>Question {i+1}:</strong> {question['question']}</p>
                    <p><strong>Your answer:</strong> <span class="{'correct-answer' if is_correct else 'wrong-answer'}">{user_answer}</span></p>
                    {'' if is_correct else f'<p><strong>Correct answer:</strong> <span class="correct-answer">{correct_answer}</span></p>'}
                </div>
                """, unsafe_allow_html=True)
            
            # Download options
            st.markdown("<h3 class='sub-header'>Download Results</h3>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); margin-bottom: 30px;">
                <p style="margin-bottom: 20px; color: #555;">Download your quiz results in your preferred format:</p>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(get_excel_download_link(
                    st.session_state.user_info,
                    st.session_state.quiz_data,
                    st.session_state.answers,
                    st.session_state.score,
                    time_taken
                ), unsafe_allow_html=True)
                
                st.markdown(get_pdf_download_link(
                    st.session_state.user_info,
                    st.session_state.quiz_data,
                    st.session_state.answers,
                    st.session_state.score,
                    time_taken
                ), unsafe_allow_html=True)
            
            with col2:
                st.markdown(get_csv_download_link(
                    st.session_state.user_info,
                    st.session_state.quiz_data,
                    st.session_state.answers,
                    st.session_state.score,
                    time_taken
                ), unsafe_allow_html=True)
                
                st.markdown(get_text_download_link(
                    st.session_state.user_info,
                    st.session_state.quiz_data,
                    st.session_state.answers,
                    st.session_state.score,
                    time_taken
                ), unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Restart options
            st.markdown("<h3 class='sub-header'>What would you like to do next?</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Take Another Quiz", key="take-another"):
                    st.session_state.page = 'home'
                    st.rerun()
            
            with col2:
                if st.button("Try Same Topic Again", key="try-again"):
                    # Reset quiz state but keep topic and difficulty
                    st.session_state.quiz_data = generate_quiz(
                        st.session_state.topic, 
                        st.session_state.difficulty
                    )
                    st.session_state.answers = {}
                    st.session_state.current_question = 0
                    st.session_state.start_time = time.time()
                    st.session_state.quiz_completed = False
                    st.rerun()
            


if __name__ == "__main__":
    main()


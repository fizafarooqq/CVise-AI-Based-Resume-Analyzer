import streamlit as st
import nltk
import spacy
nltk.download('stopwords')
spacy.load('en_core_web_sm')

import pandas as pd
import base64, random
import time, datetime
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io, random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course, web_course, android_course, ios_course, uiux_course
import os
os.environ["PAFY_BACKEND"] = "internal"
import pafy
import plotly.express as px
import youtube_dl
# This must be the first Streamlit command
st.set_page_config(page_title="AI Based Resume Analyzer", page_icon="🧠", layout="wide")


def get_table_download_link(df, filename, text):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    # href = f'<a href="data:file/csv;base64,{b64}">Download Report</a>'
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href


def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def course_recommender(course_list):
    st.subheader("**Courses & Certificates🎓 Recommendations**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course


connection = pymysql.connect(host='localhost', user='root', password='Password123')
cursor = connection.cursor()


def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills,
                courses):
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (
    name, email, str(res_score), timestamp, str(no_of_pages), reco_field, cand_level, skills, recommended_skills,
    courses)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

def career_chatbot(user_input):
    user_input = user_input.lower()

    if "resume" in user_input:
        responses = [
            "Your resume should be clear, concise, and tailored to the role you're applying for. Use bullet points, consistent formatting, and avoid clutter.",
            "Every job is unique — make sure to tailor your resume to match the job description by highlighting the most relevant skills and experiences 🔥.",
            "Whenever possible, quantify your achievements with metrics or results. For example, 'Increased user engagement by 25%' is much stronger than 'Improved engagement'.",
            "Start each bullet point with strong action verbs like 'Led', 'Developed', 'Designed', or 'Optimized' to convey impact and initiative."
        ]
        return random.choice(responses)

    elif "career" in user_input or "path" in user_input:
        responses = [
            "Exploring your career path starts with identifying your strengths, values, and interests. Think about the kind of work that excites you and aligns with your long-term goals 🧠.",
            "Internships, side projects, and volunteer roles can give you hands-on experience that helps clarify what career direction suits you best 🔑.",
            "Consider conducting informational interviews with professionals in fields you're curious about — hearing their journeys can help you make informed decisions.",
            "If you're considering a shift or want to deepen your skills, online courses, certifications, and bootcamps are excellent ways to explore new career fields 📚."
        ]
        return random.choice(responses)

    elif "interview" in user_input:
        responses = [
            "Behavioral interviews are common, so practice answering questions using the STAR method (Situation, Task, Action, Result) to structure your responses effectively.",
            "Before any interview, thoroughly research the company’s mission, recent projects, and culture. This shows genuine interest and helps you tailor your answers 🕵️‍♂️.",
            "Have at least two thoughtful questions prepared for the interviewer. Asking about team dynamics, growth opportunities, or company vision shows you're serious and engaged.",
            "Participating in mock interviews — either with a friend or mentor — is a great way to reduce nerves, refine your answers, and receive constructive feedback ✨."
        ]
        return random.choice(responses)

    else:
        responses = [
            "That’s an insightful question! If you can provide a bit more detail, I’d be happy to offer more targeted guidance ✨.",
            "Always keep learning and growing — take on real-world challenges, expand your network, and stay curious. Progress comes from consistent effort!",
            "Remember, your career is a journey. It's okay to experiment, take detours, and evolve over time. Be patient, stay focused, and trust the process 🏃‍♂️.",
            "Success isn’t an overnight event. It comes from building valuable skills, showing up consistently, and staying resilient through ups and downs 🔥."
        ]
    return random.choice(responses)

def run():
    
    # Custom CSS Styling
    st.markdown("""
        <style>
        body {
            background-color: white;
        }
        .css-18e3th9 {
            padding: 2rem 1rem 10rem 1rem;
        }
        .stApp {
            background: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333333;
        }
        h1, h2, h3, h4 {
            color: black;
        }
        .stButton>button {
            background-color: #7ca7eb;
            color: white;
            border-radius: 12px;
            padding: 0.5em 2em;
            font-size: 1em;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #7ca7eb;
            color: #white;
        }
        .css-1d391kg { 
            background-color: white; 
            border-radius: 10px; 
            padding: 1rem;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        }
        .stSidebar {
            background: #eeeeee;
            color: white;
        }
        .css-1lcbmhc {
            color: white;
        }
                
        .skill-badge {
            background-color: #7ca7eb;
            padding: 8px 16px;
            margin: 6px;
            border-radius: 20px;
            color: white;
            display: inline-block;
            font-size: 15px;
            font-weight: 600;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            transition: background-color 0.3s ease;
        }
        .skill-badge:hover {
            background-color: #7ca7e;
        }

        </style>
        """, unsafe_allow_html=True)
    
    # Create two columns
    col1, col2 = st.columns([1, 3])  # 1/3 ratio (adjust if needed)

    # In the first column: show image
    with col1:
        img = Image.open('./Logo/logo.png')
        img = img.resize((120, 120))  # Reduce size here
        st.image(img)

    # In the second column: show text
    with col2:
        st.markdown("<h1 style='text-align: left; color: black;'>CVise</h1>", unsafe_allow_html=True)

    activities = ["👤 Normal User", "🛡️ Admin"]
    choice = st.selectbox("Choose among the given options:", activities)

    st.sidebar.markdown("---")
    st.sidebar.markdown("<h2 style='color: black;'>🤖 Career Assistant Bot</h2>", unsafe_allow_html=True)
    user_question = st.sidebar.text_input("Ask me anything about your resume, career or interviews!")

    if st.sidebar.button("Get Advice"):
        if user_question:
            bot_response = career_chatbot(user_question)
            st.sidebar.success(bot_response)
        else:
            st.sidebar.warning("Please type a question!")


    # Create the DB
    db_sql = """CREATE DATABASE IF NOT EXISTS SRA;"""
    cursor.execute(db_sql)
    connection.select_db("sra")

    # Create table
    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(100) NOT NULL,
                     Email_ID VARCHAR(50) NOT NULL,
                     resume_score VARCHAR(8) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Page_no VARCHAR(5) NOT NULL,
                     Predicted_Field VARCHAR(25) NOT NULL,
                     User_level VARCHAR(30) NOT NULL,
                     Actual_skills VARCHAR(300) NOT NULL,
                     Recommended_skills VARCHAR(300) NOT NULL,
                     Recommended_courses VARCHAR(600) NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)

    if choice == '👤 Normal User':
        
        pdf_file = st.file_uploader("📄 Upload your Resume", type=["pdf"])
        if pdf_file is not None:
            save_image_path = './Uploaded_Resumes/' + pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())

            # show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()

            if resume_data:
                resume_text = pdf_reader(save_image_path)

                st.header("📊 Resume Analysis")
                st.success("Hello " + resume_data['name'])
                st.subheader("📝 Basic Info")
                try:
                    st.text('👤 Name: ' + resume_data['name'])
                    st.text('📧 Email: ' + resume_data['email'])
                    st.text('📞 Contact: ' + resume_data['mobile_number'])
                    st.text('📄 Resume Pages: ' + str(resume_data['no_of_pages']))
                except:
                    pass

                cand_level = ''
                if resume_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    st.markdown('''<h4 style='text-align: left; color: #7ca7eb;'>You are looking Fresher.</h4>''',
                                unsafe_allow_html=True)
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #7ca7eb;'>You are at intermediate level!</h4>''',
                                unsafe_allow_html=True)
                elif resume_data['no_of_pages'] >= 3:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #7ca7eb;'>You are at experience level!''',
                                unsafe_allow_html=True)

                
                st.markdown("### Skills that you have:")
                skills_html = ""
                for skill in resume_data['skills']:
                    skills_html += f'<div class="skill-badge">{skill}</div> '

                st.markdown(skills_html, unsafe_allow_html=True)


                ##  recommendation
                ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep Learning', 'flask',
                              'streamlit']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                               'javascript', 'angular js', 'c#', 'flask']
                android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
                ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
                uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
                                'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                                'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
                                'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
                                'user research', 'user experience']
                interview_questions = {
                    "Data Science": [
                        "What is overfitting in machine learning?",
                        "Explain bias-variance tradeoff.",
                        "How do you handle missing data?"
                    ],
                    "Web Development": [
                        "What is REST API?",
                        "Explain the concept of responsive design.",
                        "What is the difference between SQL and NoSQL databases?"
                    ],
                    "Android Development": [
                        "What is an Activity in Android?",
                        "What is the Android lifecycle?",
                        "Explain MVVM architecture."
                    ],
                    "IOS Development": [
                        "What is SwiftUI?",
                        "How does memory management work in iOS?",
                        "Explain MVC architecture in iOS apps."
                    ],
                    "UI-UX Development": [
                        "What is the difference between UX and UI?",
                        "Explain the design thinking process.",
                        "What tools do you prefer for prototyping?"
                    ]
                }


                recommended_skills = []
                reco_field = ''
                rec_course = ''
                ## Courses recommendation
                for i in resume_data['skills']:
                    ## Data science recommendation
                    if i.lower() in ds_keyword:
                        print(i.lower())
                        reco_field = 'Data Science'
                        st.success("** Our analysis says you are looking for Data Science Jobs.**")
                        recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
                                              'Data Mining', 'Clustering & Classification', 'Data Analytics',
                                              'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
                                              'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask",
                                              'Streamlit']
                        
                        st.markdown("### Recommended skills for you:")

                        reco_skills_html = ""
                        for skill in recommended_skills:
                            reco_skills_html += f'<div class="skill-badge">{skill}</div> '

                        st.markdown(reco_skills_html, unsafe_allow_html=True)

                        st.markdown(
                            '''<h4 style='text-align: left; color: black;'>Adding these skills to your resume will boost🚀 the chances of getting a Job💼</h4>''',
                            unsafe_allow_html=True)

                        rec_course = course_recommender(ds_course)
                        break

                    ## Web development recommendation
                    elif i.lower() in web_keyword:
                        print(i.lower())
                        reco_field = 'Web Development'
                        st.success("** Our analysis says you are looking for Web Development Jobs **")
                        recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento',
                                              'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
                       
                        st.markdown("### Recommended skills for you:")

                        reco_skills_html = ""
                        for skill in recommended_skills:
                            reco_skills_html += f'<div class="skill-badge">{skill}</div> '

                        st.markdown(reco_skills_html, unsafe_allow_html=True)

                        st.markdown(
                            '''<h4 style='text-align: left; color: black;'>Adding these skills to your resume will boost🚀 the chances of getting a Job💼</h4>''',
                            unsafe_allow_html=True)

                        rec_course = course_recommender(ds_course)
                        break

                    ## Android App Development
                    elif i.lower() in android_keyword:
                        print(i.lower())
                        reco_field = 'Android Development'
                        st.success("** Our analysis says you are looking for Android App Development Jobs **")
                        recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java',
                                              'Kivy', 'GIT', 'SDK', 'SQLite']
                       
                        st.markdown("### Recommended skills for you:")

                        reco_skills_html = ""
                        for skill in recommended_skills:
                            reco_skills_html += f'<div class="skill-badge">{skill}</div> '

                        st.markdown(reco_skills_html, unsafe_allow_html=True)

                        st.markdown(
                            '''<h4 style='text-align: left; color: black;'>Adding these skills to your resume will boost🚀 the chances of getting a Job💼</h4>''',
                            unsafe_allow_html=True)

                        rec_course = course_recommender(ds_course)
                        break

                    ## IOS App Development
                    elif i.lower() in ios_keyword:
                        print(i.lower())
                        reco_field = 'IOS Development'
                        st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                        recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode',
                                              'Objective-C', 'SQLite', 'Plist', 'StoreKit', "UI-Kit", 'AV Foundation',
                                              'Auto-Layout']
                       
                        st.markdown("### Recommended skills for you:")

                        reco_skills_html = ""
                        for skill in recommended_skills:
                            reco_skills_html += f'<div class="skill-badge">{skill}</div> '

                        st.markdown(reco_skills_html, unsafe_allow_html=True)

                        st.markdown(
                            '''<h4 style='text-align: left; color: black;'>Adding these skills to your resume will boost🚀 the chances of getting a Job💼</h4>''',
                            unsafe_allow_html=True)

                        rec_course = course_recommender(ds_course)
                        break

                    ## Ui-UX Recommendation
                    elif i.lower() in uiux_keyword:
                        print(i.lower())
                        reco_field = 'UI-UX Development'
                        st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                        recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq',
                                              'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing',
                                              'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe',
                                              'Solid', 'Grasp', 'User Research']
                        
                        st.markdown("### Recommended skills for you:")

                        reco_skills_html = ""
                        for skill in recommended_skills:
                            reco_skills_html += f'<div class="skill-badge">{skill}</div> '

                        st.markdown(reco_skills_html, unsafe_allow_html=True)

                        st.markdown(
                            '''<h4 style='text-align: left; color: black;'>Adding these skills to your resume will boost🚀 the chances of getting a Job💼</h4>''',
                            unsafe_allow_html=True)

                        rec_course = course_recommender(ds_course)
                        break

                ## Insert into table
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date + '_' + cur_time)

                ### Resume writing recommendation
                st.subheader("**Resume Tips & Ideas💡**")
                resume_score = 0
                if 'Objective' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #7ca7eb;'>[+] Awesome! You have added Objective</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #402924;'>[-] According to our recommendation please add your career objective, it will give your career intension to the Recruiters.</h4>''',
                        unsafe_allow_html=True)

                if 'Experience' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #7ca7eb;'>[+] Awesome! You have added Experience.</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #402924;'>[-] According to our recommendation please add Experience.</h4>''',
                        unsafe_allow_html=True)

                if 'Hobbies' or 'Interests' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #7ca7eb;'>[+] Awesome! You have added your Hobbies⚽</h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #402924;'>[-] According to our recommendation please add Hobbies⚽. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',
                        unsafe_allow_html=True)

                if 'Achievements' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #7ca7eb;'>[+] Awesome! You have added your Achievements🏅 </h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #402924;'>[-] According to our recommendation please add Achievements🏅. It will show that you are capable for the required position.</h4>''',
                        unsafe_allow_html=True)

                if 'Projects' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown(
                        '''<h4 style='text-align: left; color: #7ca7eb;'>[+] Awesome! You have added your Projects👨‍💻 </h4>''',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '''<h4 style='text-align: left; color: #402924;'>[-] According to our recommendation please add Projects👨‍💻. It will show that you have done work related the required position or not.</h4>''',
                        unsafe_allow_html=True)

                st.subheader("**Resume Score📝**")
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #7ca7eb;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                )
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score += 1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)
                st.success('** Your Resume Writing Score: ' + str(score) + '**')
                st.warning(
                    "** Note: This score is calculated based on the content that you have added in your Resume. **")

                st.subheader("🎤 Practice Interview Questions")
                if reco_field in interview_questions:
                    questions = random.sample(interview_questions[reco_field], 3)
                    for q in questions:
                        st.write(f"- {q}")


                insert_data(resume_data['name'], resume_data['email'], str(resume_score), timestamp,
                            str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']),
                            str(recommended_skills), str(rec_course))

            else:
                st.error('❌ Something went wrong. Please try again.')

    else:
        st.success('🔒 Welcome to Admin Side')

        ad_user = st.text_input("👤 Username")
        ad_password = st.text_input("🔒 Password", type='password')

        if st.button('Login'):
            if ad_user == 'fiza' and ad_password == '12345':
                st.success("Welcome Admin 🚀")

                cursor.execute('''SELECT*FROM user_data''')
                data = cursor.fetchall()
                st.header("📚 Users' Data")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                                                 'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
                                                 'Recommended Course'])
                st.dataframe(df)

                st.markdown(get_table_download_link(df, 'User_Data.csv', '📥 Download Report'), unsafe_allow_html=True)

                plot_data = pd.read_sql('SELECT * FROM user_data', connection)

                st.subheader("📈 Predicted Field Pie-Chart")
                fig = px.pie(df, values=plot_data['Predicted_Field'].value_counts(), 
                             names=plot_data['Predicted_Field'].unique(), title='Predicted Field Distribution')
                st.plotly_chart(fig)

                st.subheader("📈 User Experience Level Pie-Chart")
                fig2 = px.pie(df, values=plot_data['User_level'].value_counts(), 
                             names=plot_data['User_level'].unique(), title='Experience Level Distribution')
                st.plotly_chart(fig2)

            else:
                st.error("❌ Wrong Username or Password")

run()


Key Functionalities
1) Resume Upload and Parsing:

    Users upload their resume in PDF format.

    The app extracts structured data (name, email, phone, number of pages, skills, etc.) using pyresparser.

2) Resume Content Analysis:

    Text is extracted using pdfminer3.

    The app checks for key sections like Objective, Experience, Projects, Hobbies, and Achievements.

    It assigns a Resume Score out of 100 based on presence of these sections.

3) Candidate Profiling:

    Categorizes users as Fresher, Intermediate, or Experienced based on resume length.

    Displays uploaded skills with attractive skill badges.

4) Field Prediction and Skill Recommendation:

    Predicts the candidate’s target field (e.g., Data Science, Web Dev, Android, iOS, UI/UX) based on detected skills.
    
    Recommends in-demand skills relevant to the predicted field.

5) Course Recommendations:

    Dynamically suggests online courses to help bridge the skill gap.
    
    Users can choose how many recommendations to see via a slider.

6) Interview Preparation:

    Offers 3 randomized interview questions tailored to the predicted field.

7) Career Assistant Chatbot:

    Sidebar chatbot that answers queries about resumes, careers, or interviews.
    
    Provides friendly, insightful, and motivational responses.

8) Database Integration:

    Stores each user’s submission in a MySQL database (user_data table).
    
    Captures: name, email, resume score, page count, field, experience level, skills, and recommendations.

9) Admin Dashboard:

    Secured login for admin (Username: fiza, Password: 12345).
    
    Displays all user submissions in a tabular view.
    
    Enables CSV download of all records.

    Displays two Pie Charts:
    
    Predicted Field Distribution
    
    User Experience Level Distribution


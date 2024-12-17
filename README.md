# TASKFLOW
#### Video Demo:  <URL HERE>
#### Description:

**TaskFlow** is a web-based **Task Management System** designed to enhance personal productivity by helping users organize their tasks and capture fleeting ideas. It features a secure and user-friendly platform where users can manage tasks and store temporary thoughts, ensuring an efficient workflow. The application prioritizes security, simplicity, and scalability, making it a robust tool for anyone looking to stay organized.

## Features  

- **User Authentication**:  
  - Secure user registration with validation to avoid duplicate usernames or emails.  
  - Login functionality with password hashing to store passwords securely.  
  - Logout functionality to terminate the session securely.

- **Task Management**:  
  - Users can create, update, and delete tasks.  
  - Tasks are linked to specific users, ensuring data privacy and organization.  

- **Quick Thoughts**:  
  - A dedicated section to capture fleeting thoughts or reminders.  
  - Quick thoughts can be created, updated, or deleted with ease.

- **Error Handling**:  
  - Strict access control ensures users can only manage their own data.  
  - Flash messages provide immediate feedback on user actions, including success and error notifications.

- **Responsive Design** (Planned):  
  - A mobile-friendly interface for better accessibility on various devices.

## File Descriptions  

### **1. `app/routes.py`**  
Contains the main routes for user requests and functionality:
- Handles user authentication, session management, and CRUD operations for tasks and quick thoughts.
- Renders dynamic templates, such as task lists and forms for creating or editing tasks/quick thoughts.

### **2. `app/templates/quick_thought.html`**  
Displays the interface for managing Quick Thoughts:
- Users can add, edit, and delete thoughts using an easy-to-navigate form.

### **3. `app/templates/index.html`**  
The main dashboard template that links users to both task management and the Quick Thoughts section.

### **4. `app/forms.py`**  
Contains form classes used across the app:
- `LoginForm` for handling user authentication.
- `RegistrationForm` for secure user registration.
- `TaskForm` for task creation and editing.
- `QuickThoughtForm` for adding/editing quick thoughts.

### **5. `app/models.py`**  
Defines the database schema and relationships:
- **User**: Stores user information (username, email, password).
- **Task**: Stores tasks and links them to the respective users.
- **QuickThought**: Stores temporary notes or thoughts for users.

### **6. `README.md`**  
This file, providing a comprehensive overview of the project, its functionalities, and design decisions.

## Design Choices  

1. **Security**:  
   - Passwords are securely hashed using `generate_password_hash` to prevent unauthorized access.  
   - Registration includes checks to ensure no duplicate usernames or emails.  
   - Users can only access their own data, ensuring privacy and security.

2. **User Experience**:  
   - Simple, intuitive UI for managing tasks and thoughts.
   - Flash messages provide users with immediate feedback on actions like task creation or error handling.

3. **Scalability**:  
   - Flask's modular structure allows easy addition of features.
   - The relational database schema is flexible and can be expanded without major architectural changes.

4. **Error Handling**:  
   - Graceful error messages are displayed when users attempt unauthorized actions or access missing resources.

## Future Improvements  

- **Responsive Design**:  
  - Enhance mobile responsiveness for improved usability across different screen sizes.

- **Search and Filters**:  
  - Implement task search and filtering options, such as by due date, priority, or task status.

- **Task Prioritization**:  
  - Enable users to assign priority levels to tasks for better organization.

- **Notifications**:  
  - Integrate reminders for upcoming tasks and deadlines.

- **Dark Mode**:  
  - Offer a dark theme for improved usability in low-light conditions.

## Conclusion  

This project showcases the integration of Flask, SQLAlchemy, and essential web development practices to create a functional task management system. It prioritizes security, usability, and scalability, providing a solid foundation for further enhancements. With features like task management, quick thoughts capture, and user authentication, **TaskFlow** is an ideal tool for staying organized.

Feedback and contributions are welcome to help improve and expand this project further.

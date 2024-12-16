# Django REST Framework with Celery for Background Processing

This project is a Django-based API designed to process requests asynchronously using **Celery** and **Redis**. It provides immediate responses to API requests while handling long-running tasks in the background.

---

## Prerequisites

### Base OS
- Any (Linux is recommended for production)
- **Python 3.11+**
- **Redis** (for task queue management)
#Steps to run the project
1. Clone the Repository
   
#2. Set Up a Virtual Environment
   
   python3 -m venv venv (Creating the Virtual Enviroment)
   source venv/bin/activate   On Windows: venv\Scripts\activate  (To activate the Virtual Enviroment)
   
#3. Install Python Dependencies

   pip install -r requirements.txt

#4.  Install and start Redis

   On Ubuntu
   sudo apt update
   sudo apt install redis
   sudo systemctl start redis
   sudo systemctl enable redis
   
   (redis should run before django server and celery and it should run on port 6379 for example:)
   docker run -d -p 6379:6379 redis (locally, we use "redis-server" on separated terminal and it automatically runs on port 6379)

#5. Start the Django Development Server
   python manage.py runserver 80       (80 is the port Number)
   
#6. Start the Celery worker
   celery -A LittleBirdie worker --loglevel=info
   


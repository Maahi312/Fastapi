
# CI/CD Pipeline for FastAPI using Jenkins, Docker & GitHub

This project demonstrates a fully automated **CI/CD pipeline** for deploying a FastAPI application using **Docker**, **Jenkins**, and **GitHub** on an **Ubuntu server**.

## 📂 Project Structure
```
Jenkins_CICD/
├── .gitignore
├── Dockerfile
├── Jenkinsfile
├── main.py
└── requirements.txt
```

## 📋 Prerequisites
- Python 3.11 (Local)
- Git & GitHub Account
- Ubuntu 22.04 Droplet (e.g., DigitalOcean) with root SSH access
- Jenkins Installed on Server
- Docker Installed on Server
- Personal Access Token (PAT) for GitHub (Repo scope)

## ⚙️ Local FastAPI Setup
1. **Create Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Unix/macOS
    venv\Scripts\activate     # For Windows
    ```

2. **Install Dependencies**
    ```bash
    pip install fastapi uvicorn
    pip freeze > requirements.txt
    ```

3. **Application Code (`main.py`)**
    ```python
    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"message": "Hello, Welcome to Jenkins, CI/CD pipeline"}
    ```

4. **Run Locally**
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
    Access: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🗂️ Version Control & GitHub
1. **Initialize Git Repo**
    ```bash
    git init
    git add .
    git commit -m "Initial FastAPI setup"
    ```

2. **Push to GitHub**
    ```bash
    git remote add origin https://github.com/<yourusername>/<your-repo>.git
    git branch -M master
    git push -u origin master
    ```

3. **Generate Personal Access Token (PAT)**
    - Navigate: GitHub » Settings » Developer Settings » Tokens (Classic)
    - Select `repo` scope.
    - Save token for Jenkins credentials.

## 🖥️ Jenkins Server Provisioning
1. **SSH into Server**
    ```bash
    ssh root@<your_droplet_ip>
    ```

2. **Install Java & Jenkins**
    ```bash
    sudo apt update
    sudo apt install -y openjdk-17-jdk wget gnupg
    # Add Jenkins Repo & Key
    # [Insert Jenkins repo key steps as in documentation]
    sudo apt install -y jenkins
    sudo systemctl enable --now jenkins
    sudo ufw allow 8080
    ```

3. **Unlock Jenkins**
    ```bash
    sudo cat /var/lib/jenkins/secrets/initialAdminPassword
    ```

## 🐳 Docker on Jenkins Host
1. **Install Docker**
    ```bash
    sudo apt install -y docker.io
    sudo systemctl enable --now docker
    ```

2. **Grant Jenkins Access to Docker**
    ```bash
    sudo usermod -aG docker jenkins
    sudo systemctl restart jenkins
    ```

## 🛠️ CI/CD Configuration Files
### Dockerfile
```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Jenkinsfile
```groovy
pipeline {
  agent any
  environment {
    IMAGE_NAME     = "fastapi-jenkins"
    CONTAINER_NAME = "fastapi_app"
    APP_PORT       = "8000"
  }
  stages {
    stage('Checkout') {
      steps { git url: 'https://github.com/<yourusername>/<your-repo>.git', credentialsId: 'github-pat' }
    }
    stage('Build Image') {
      steps { sh 'docker build -t $IMAGE_NAME .' }
    }
    stage('Replace Container') {
      steps {
        sh '''
          docker stop $CONTAINER_NAME || true
          docker rm   $CONTAINER_NAME || true
          docker run -d --name $CONTAINER_NAME -p $APP_PORT:$APP_PORT $IMAGE_NAME
        '''
      }
    }
  }
  post {
    success { echo "✅ Deployment succeeded; app is live on port $APP_PORT" }
    failure { echo "❌ Deployment failed; check logs" }
  }
}
```

## 🔄 Configure Jenkins Pipeline
1. **Add GitHub PAT Credentials**
    - Manage Jenkins » Credentials » Add (Username & PAT as Password)
2. **Create Pipeline Job**
    - New Item » Pipeline » Definition: Pipeline script from SCM
    - SCM: Git, Repo URL, Credentials: github-pat
    - Script Path: Jenkinsfile
3. **Save & Build Now**

## ✅ Deployment Verification
- Check running container:
    ```bash
    docker ps
    ```
- Visit: `http://<droplet_ip>:8000/`

## 🔄 Updating & Redeployment
1. Modify code (e.g., update greeting in `main.py`)
2. Push changes:
    ```bash
    git commit -am "Updated greeting"
    git push
    ```
3. Jenkins will auto-deploy or trigger **Build Now**.

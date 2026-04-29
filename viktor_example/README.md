---

# Viktor Sample App

This repository contains a simple example application for the **Viktor.ai platform**.

It demonstrates how to build a basic **Editor-type app** using the Viktor framework.  
This project is intended as a minimal tutorial to help you understand the key steps required to create, configure, and publish a Viktor app.

---

## 🔑 Access Token

Use the following token when required:

```python
FGAGAFWERFEAGASDGASDWETEWGDASGDASGASDFGASF (SAMPLE)
```

---

# 🚀 How to Build the Simple Viktor App

## Step 1 — Create the App Locally

### 1️⃣ Create Project Directories

```bash
C:\Users\<username>\viktor-apps
C:\Users\<username>\viktor-apps\simple-app
```

Navigate to your project folder and create the app:

```bash
viktor-cli create-app --app-type editor -init
```

⚠️ **Important:** You must use `editor` as the app type.

---

### 2️⃣ Update `requirements.txt`

Add the following content:

```text
viktor==X.X.X   <-- Don't modify this line
plotly
pandas
```

✅ Do not change the `viktor==X.X.X` line.

---

### 3️⃣ Copy Required Files

Make sure to copy all necessary files into your project directory, including:

- Core application files
- Configuration files
- Any required image assets

⚠️ Do not forget image resources if your app depends on them.

---

### 4️⃣ Clear, Install, and Start

Before running the app, clear any previous builds:

```bash
viktor-cli clear
```

Then install dependencies:

```bash
viktor-cli install
```

Start the application:

```bash
viktor-cli start
```

---

# 🌍 Step 2 — Publish the App Online

### 1️⃣ Check Available Apps

```bash
viktor-cli apps
```

This shows your registered apps.

---

### 2️⃣ Publish the App

```bash
viktor-cli publish --registered-name data-analysis-tutorial --tag v0.1.0
```

This command publishes version `v0.1.0` of your app to the Viktor platform.

---

# ✅ Summary

This example demonstrates:

- Creating an **Editor-type Viktor app**
- Managing dependencies
- Running the app locally
- Publishing the app to the Viktor platform

---

If you have any questions about Viktor development, feel free to explore the official Viktor documentation or open an issue in this repository.

---

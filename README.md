# SafeHome - Home Security and Surveillance System

**KAIST CS350 Software Engineering - Team 9 Project (Fall 2025)**

SafeHome is a comprehensive home security and surveillance system designed to protect your property and provide peace of mind. The system integrates security management and surveillance capabilities into a single, easy-to-use platform accessible both locally through a control panel and remotely through a web browser.

## Features

### Security Management
- **Multiple Security Modes**
  - Away Mode: Full protection when the house is unoccupied
  - Stay Mode: Perimeter protection while occupants are inside
  - Disarm Mode: System deactivated for normal access
- **Safety Zone Management**: Create and manage multiple safety zones, assign sensors
- **Intrusion Detection**: Real-time monitoring with configurable entry delay and automatic monitoring service notification
- **Panic Button**: Emergency alarm trigger for immediate response

### Surveillance Management
- **Camera Control**: View individual cameras or thumbnail overview with pan/zoom controls
- **Multiple Viewing Options**: Floor plan-based selection, thumbnail view, real-time video feed
- **Password Protection**: Secure camera access control

### Dual Interface Access
- **Control Panel (Desktop)**: Native Tkinter-based GUI with full system control
- **Web Interface (Browser)**: Remote access with two-step authentication

## System Requirements

### Software Requirements
- **Python**: 3.10 or higher (3.11 recommended)
- **Operating System**: Windows 10+, macOS 10.14+, or Ubuntu 20.04+
- **Web Browser**: Chrome 90+, Firefox 88+, Edge 90+, Safari 14+

### Hardware Requirements
- **Minimum**: Intel Core i3, 4GB RAM, 500MB storage
- **Recommended**: Intel Core i5, 8GB RAM, 1GB storage

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/SafeHome_team9.git
cd SafeHome_team9
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup (Optional)
The database is created automatically on first run. For migration:
```bash
python common/migrate_database.py
```

### 5. Create Web User Account (Optional)
```bash
python common/create_web_user.py
```

## Quick Start

### Starting the System
```bash
python main.py
```

You should see:
```
==================================================
SafeHome Control Panel Started
System Status: OFF (Press 'Turn On' to start)
Web Interface: http://localhost:5000
==================================================
```

### Default Credentials

**Control Panel:**
- Username: `admin`
- Password: `1234`

**Web Interface:**
- Username: `homeowner`
- First Password: `first123`
- Second Password: `second456`

> **Important**: Change these default passwords immediately after first login!

## Project Structure

```
SafeHome_team9/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── safehome.db            # SQLite database (auto-generated)
├── common/                 # Shared utilities and database management
├── control_panel/          # Desktop GUI (Tkinter)
├── web/                    # Web interface (Flask)
├── security/               # Security system logic
├── surveillance/           # Camera and surveillance management
├── tests/                  # Unit and integration tests
├── docs/                   # Documentation
└── virtual_device_v4/      # Simulated device resources
```

## System Architecture

SafeHome consists of several integrated components:

- **Authentication System**: User login and access control
- **Security System**: Core security logic, alarm management, and zone control
- **Surveillance System**: Camera management and video feed handling
- **Configuration Manager**: System settings and safety zone management
- **Storage Manager**: Database persistence for users, settings, and logs
- **Event Logging**: Comprehensive audit trail of all system events

## Usage Guide

### Control Panel
1. Click "Turn On" to start the system
2. Login with your credentials
3. Navigate using the main menu:
   - **SECURITY**: Manage safety zones
   - **SURVEILLANCE**: Configure security modes
   - **CONFIGURE**: System settings and logs

### Web Interface
1. Open browser and navigate to `http://localhost:5000`
2. Complete two-step authentication
3. Use dashboard for:
   - Arm Away/Stay modes
   - Disarm system
   - Panic alarm
   - Surveillance access
   - Zone management

## Testing

Run the test suite:
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

## Troubleshooting

### Common Issues

**System Won't Start:**
- Verify Python 3.10+ is installed: `python --version`
- Check dependencies: `pip list | grep Flask`
- Reinstall if needed: `pip install -r requirements.txt --force-reinstall`

**Login Issues:**
- Account locked after 5 failed attempts
- Unlock script: `python common/unlock_admin_cp.py`

**Web Interface Not Accessible:**
- Ensure Control Panel is running
- Check if port 5000 is available
- Try: `http://localhost:5000`

**Port Conflict:**
- Another application may be using port 5000
- Modify port in `main.py` if needed

## Documentation

Detailed documentation is available in the `docs/` folder:
- User Manual: `Team9_User_Manual_Document.pdf`
- SRS Document: `docs/SRS_document.doc`
- SDS Document: `docs/SDS_document.docx`
- Test Documentation: `docs/UNIT_TEST_DOCUMENTATION_UPDATED.md`

## Security Notes

- Change default passwords immediately after installation
- Use strong, unique passwords
- Account lockout protection enabled (5 failed attempts)
- Two-step authentication for web access
- All login attempts are logged

## Team Members

**Team 9 - KAIST CS350 Fall 2025**

## License

This project is developed for educational purposes as part of KAIST CS350 Software Engineering course.

---

For more information, please refer to the [User Manual](Team9_User_Manual_Document.pdf).

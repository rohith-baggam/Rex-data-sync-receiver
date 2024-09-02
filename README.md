# REX: Seamless Django Database Transformation and Migration (Receiver)

Effortlessly migrate and synchronize data between Django projects across servers and databases, with enhanced security and real-time communication.

## 🚀 Introduction

REX is a powerful tool designed to facilitate seamless data migration between Django projects, whether on the same or different servers, supporting cross-database transfers between PostgreSQL, SQL, and more. This README is specifically for the **receiver** part of the REX project, which is responsible for receiving and validating the migrated data. REX handles the complexity of synchronizing both the database schema and the data itself, ensuring a smooth transition, even between different database systems. With built-in encryption and real-time communication via WebSockets, REX offers a secure and reliable solution for data transfer.

## ✨ Key Features

- **Cross-Database Compatibility**: The receiver is equipped to handle data from various database systems, transforming it into a compatible format for seamless integration into the destination Django project.
- **End-to-End Encryption**: Ensure your data remains secure throughout the migration process with robust encryption. REX uses private and public keys for secure synchronization, allowing only authorized projects to connect and transfer data.
- **Real-Time Communication**: Leveraging WebSockets, REX provides real-time feedback during the data transfer process, from initial schema verification to final data synchronization.
- **Schema Verification**: The receiver validates the incoming schema against its own models, ensuring compatibility and preventing data inconsistencies.
- **Transaction Management**: The entire migration is managed within a transaction, allowing for rollbacks in case of errors, ensuring data integrity and security.

## 🛠 Installation

Before getting started, install the necessary dependencies:

```bash

pip install -r requirements.txt

```

Ensure that Redis is installed and running, as it is required for WebSocket communication:

```bash

brew install redis

```

## 🔧 Configuration

In your `.env` file, configure the following settings:

```bash

REDIS_PORT=redis://127.0.0.1:6379
SECRET_KEY=your-django-secret-key
DATA_SYNC_RECEIVER_TOKEN=your-unique-receiver-token

```

Ensure both the sender and receiver projects have matching `DATA_SYNC_RECEIVER_TOKEN` and `SECRET_KEY` values.

Settings Example:

```python

INSTALLED_APPS = [
    "daphne",
    'corsheaders',
    'django_data_seed',
    # other apps
]

```

## ⚙️ How It Works

1. **Token and Key Validation**: The receiver server exchanges tokens with the sender (defined in `.env`). If the tokens match, the connection is established. Once the tokens are verified, both servers validate their `SECRET_KEY` settings to confirm compatibility.
2. **Schema Verification**: The receiver server accepts the schema from the sender, validating each model and field. All schema properties are encrypted before transmission, ensuring data security.
3. **Data Synchronization**: Upon successful schema validation, the receiver server decrypts and processes the data in JSON format, incrementally importing it into the destination database.
4. **Progress Tracking**: The receiver provides real-time updates on the data transfer progress, ensuring transparency throughout the synchronization process.
5. **Completion**: Once data synchronization is complete, the receiver server confirms the success, and the transaction is committed, securing the newly transferred data.

## 🎛 Web Interface

- **Connection Establishment**: View real-time messages as the receiver and sender establish communication.
- **Schema Validation**: Receive live feedback during schema verification.
- **Data Transfer**: Monitor the percentage of data transferred and track the overall progress.

## 🧩 Packages Used

- `channels==4.1.0`
- `channels-redis==4.2.0`
- `cryptography==42.0.7`
- `daphne==4.1.2`
- `django-data-seed==0.4.1`
- `djangorestframework==3.15.2`
- `redis==5.0.8`
- `websockets==12.0`

## Testing

- To ensure the setup and communication logic are working as expected, use the following command:

```bash

python3 manage.py test

```

## 🗂 Supported Versions

- **Django Versions**:
  - Django 3.2
  - Django 4.x
- **Python Versions**:
  - Python 3.7 - 3.10
- **Databases**:
  - PostgreSQL
  - MySQL
  - SQLite

## 🛡 Security & Permissions

REX ensures robust security by requiring:

- **Token-Based Validation**: Sender and receiver servers must exchange a pre-shared token to initiate communication.
- **Schema Verification**: The receiver server verifies that both databases have matching schemas before data synchronization begins.
- **Encrypted Data Transfer**: All data, including schema information and individual objects, is encrypted during transmission using the public/private key system.

With REX, receiving data from other Django projects is transformed into a seamless, secure, and efficient operation. Whether you're synchronizing data across servers or integrating different database types, REX takes care of everything—from schema validation to real-time data synchronization—all within the safety of an encrypted connection.

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## 🛠 Support

For any issues or questions, open an issue on the GitHub repository.

## 👤 Author

**Rohith Baggam**

LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/rohith-baggam/)

## 🎨 Frontend Design

The frontend Figma design and development were contributed by:

- [Frontend GitHub Profile](https://github.com/samasarunreddy/Data_sync)
- [Figma Design Link](https://www.figma.com/design/lcAVBTVFooPSZxiiJJm3fg/Projects?node-id=60-2&t=GtEGEGXnPc58x9VO-1)

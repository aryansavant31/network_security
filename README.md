# Phishing Detection Project

An end-to-end machine learning project for detecting phishing or unsafe network activity from structured URL/network features. The project includes data ingestion from MongoDB, data validation, feature transformation, model selection/training, MLflow/DagsHub experiment tracking, S3 artifact syncing, a FastAPI service for training and batch prediction, and AWS deployment through GitHub Actions, Amazon ECR, and EC2.

## Features

- Upload CSV data into MongoDB with an ETL script.
- Train a classification model from MongoDB data.
- Validate schema and detect data drift with the Kolmogorov-Smirnov test.
- Impute missing values with `KNNImputer`.
- Compare multiple scikit-learn models using configured hyperparameters.
- Track metrics in MLflow through DagsHub.
- Save the final preprocessing and model pipeline as `final_model/classifier.pkl`.
- Run batch predictions through a FastAPI `/predict` endpoint.
- Sync training and prediction artifacts to AWS S3.
- Deploy the containerized FastAPI application to AWS using GitHub Actions, Amazon ECR, and EC2.

## Project Structure

```text
.
├── app.py                         # FastAPI application
├── main.py                        # Training pipeline entry point
├── etl_pipeline.py                # CSV to MongoDB ingestion script
├── config/
│   └── config.yaml                # Pipeline configuration
├── network_data/
│   ├── phisingData.csv            # Source dataset used by ETL
│   └── test.csv                   # Sample prediction input
├── src/
│   └── phishingdetection/
│       ├── components/            # Data ingestion, validation, transformation, training, prediction
│       ├── constants/             # Pipeline constants
│       ├── entity/                # Config and artifact dataclasses
│       ├── exceptions/            # Custom exception handling
│       ├── logging/               # Project logging setup
│       ├── manager/               # Configuration managers
│       ├── pipelines/             # Training and prediction orchestration
│       ├── utils/                 # Common helpers and ML utilities
│       └── cloud/                 # S3 sync helper
├── final_model/                   # Saved production model
├── training_artifacts/            # Generated training artifacts
├── prediction_artifacts/          # Generated prediction artifacts
├── .github/
│   └── workflows/
│       └── main.yaml              # GitHub Actions CI/CD workflow for AWS deployment
├── schema.yaml                    # Expected input schema
├── model_hyperparams.yaml         # Model search parameters
├── requirements.txt
└── setup.py
```

## Pipeline Flow

### Training

1. Read training records from MongoDB.
2. Save raw data into the feature store.
3. Split data into train and test CSV files.
4. Validate column counts and check train/test drift.
5. Split features from the `Result` target column.
6. Impute missing feature values with KNN imputation.
7. Train and compare these models:
   - Logistic Regression
   - K-Nearest Neighbors
   - Decision Tree
   - AdaBoost
   - Gradient Boosting
   - Random Forest
8. Track precision, recall, and F1 score in MLflow.
9. Save the best model pipeline to `final_model/classifier.pkl`.
10. Sync artifacts and final model files to S3.

### Prediction

1. Read the uploaded CSV file.
2. Load baseline data from MongoDB.
3. Validate the uploaded file against the training schema.
4. Load `final_model/classifier.pkl`.
5. Append a `Prediction` column.
6. Save the output CSV under `prediction_artifacts/`.
7. Return an HTML table from the FastAPI endpoint.

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows PowerShell
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
MONGO_DB_URI=your_mongodb_connection_string
MLFLOW_URI_DAGSHUB=your_mlflow_tracking_uri
REPO_OWNER=your_dagshub_username_or_org
```

For S3 syncing, also configure AWS credentials for the AWS CLI:

```bash
aws configure
```

The current S3 bucket constant is:

```text
aryansavant31-networksecurity
```

Update the bucket name in `src/phishingdetection/constants/training_pipeline/__init__.py` and `src/phishingdetection/constants/prediction_pipeline/__init__.py` if you want to use a different bucket.

## Load Data into MongoDB

Run the ETL script to upload `network_data/phisingData.csv` into MongoDB:

```bash
python etl_pipeline.py
```

By default, this uploads records to:

```text
Database: AryanSavant
Collection: NetworkData
```

## Train the Model

You can start training from the command line:

```bash
python main.py
```

Or run the FastAPI app and use the `/train` route:

```bash
python app.py
```

Then open:

```text
http://localhost:8000/train
```

Training generates timestamped artifacts under `training_artifacts/` and writes the final model to:

```text
final_model/classifier.pkl
```

## Run the API

Start the FastAPI server:

```bash
python app.py
```

The API will be available at:

```text
http://localhost:8000
```

FastAPI documentation is available at:

```text
http://localhost:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Redirects to `/docs` |
| `GET` | `/train` | Runs the full training pipeline |
| `POST` | `/predict` | Accepts a CSV file and returns predictions as an HTML table |

## AWS Deployment (currently under works)

This project includes an AWS deployment workflow using GitHub Actions, Amazon ECR, and an EC2 instance. The deployment setup is currently under works, and the workflow is maintained in the repository under GitHub Actions.

The deployment workflow is located at:

```text
.github/workflows/main.yaml
```

The CI/CD flow is:

1. Push code changes to GitHub.
2. GitHub Actions starts the workflow defined in `.github/workflows/main.yaml`.
3. The workflow authenticates with AWS.
4. Docker builds an image for the FastAPI application.
5. The image is tagged and pushed to Amazon Elastic Container Registry.
6. The EC2 instance pulls the latest image from ECR.
7. The running container on EC2 is stopped and replaced with the new image.
8. The FastAPI application becomes available from the EC2 host.

Typical AWS resources needed for this setup:

- Amazon ECR repository to store Docker images.
- EC2 instance to run the API container.
- IAM user or role with permissions for ECR and EC2 deployment actions.
- Security group allowing inbound traffic on the application port, usually `8000`.
- GitHub repository secrets for AWS credentials and deployment configuration.

Recommended GitHub Actions secrets:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
AWS_ECR_LOGIN_URI
ECR_REPOSITORY_NAME
EC2_HOST
EC2_USERNAME
EC2_SSH_KEY
```

The exact secret names can be changed later to match the final workflow file.

A typical deployment command sequence inside GitHub Actions is:

```bash
docker build -t <ecr-repository-name> .
docker tag <ecr-repository-name>:latest <aws-account-id>.dkr.ecr.<region>.amazonaws.com/<ecr-repository-name>:latest
docker push <aws-account-id>.dkr.ecr.<region>.amazonaws.com/<ecr-repository-name>:latest
```

On EC2, the deployment step pulls and runs the image:

```bash
docker pull <aws-account-id>.dkr.ecr.<region>.amazonaws.com/<ecr-repository-name>:latest
docker stop networksecurity || true
docker rm networksecurity || true
docker run -d --name networksecurity -p 8000:8000 --env-file .env <aws-account-id>.dkr.ecr.<region>.amazonaws.com/<ecr-repository-name>:latest
```

Make sure the EC2 instance has Docker installed and has permission to pull images from ECR.

## Prediction Input Format

Prediction CSV files must follow the feature schema defined in `schema.yaml`. The target column `Result` should not be included for prediction input.

Example input file:

```text
network_data/test.csv
```

Using the FastAPI docs UI:

1. Start the app with `python app.py`.
2. Open `http://localhost:8000/docs`.
3. Expand `POST /predict`.
4. Upload a CSV file with the expected feature columns.
5. Execute the request.

The prediction output is saved under:

```text
prediction_artifacts/<timestamp>/3_model_prediction/output.csv
```

## Configuration Files

- `config/config.yaml` controls train/test split ratio, imputer parameters, and expected model accuracy.
- `schema.yaml` defines the expected feature columns and data types.
- `model_hyperparams.yaml` defines model hyperparameter grids used during model selection.

## Important Notes

- The training pipeline expects data to already exist in MongoDB. Run `etl_pipeline.py` before training if the collection is empty.
- The prediction pipeline expects `final_model/classifier.pkl` to exist. Run training first if the model file is missing.
- Artifact syncing uses the AWS CLI through `aws s3 sync`, so AWS CLI must be installed and authenticated for cloud sync to work.
- MLflow tracking is initialized through DagsHub. Make sure your DagsHub and MLflow environment variables are valid before training.
- The source code package now lives in `src/phishingdetection/`.
- AWS deployment is handled through the GitHub Actions workflow at `.github/workflows/main.yaml` and is currently under works.
- The repository includes generated artifacts and logs. For cleaner version control, consider ignoring runtime folders such as `logs/`, `training_artifacts/`, `prediction_artifacts/`, `__pycache__/`, and generated model pickle files.

## License

This project is licensed under the terms included in the `LICENSE` file.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

# STEP 1: Load and prepare the dataset
wazuh = pd.read_csv("generated_5000_logs.csv")

wazuh = wazuh.rename(columns={
    '_source.data.url': 'url',
    '_source.rule.firedtimes': 'firedtimes',
    '_source.rule.level': 'level',
    'label': 'label'
})

# Encode the label
wazuh['label'] = wazuh['label'].map({'real threat': 1, 'false positive': 0})

# Define features and label
X = wazuh[['url', 'firedtimes', 'level']]
y = wazuh['label']

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('text', TfidfVectorizer(), 'url'),
        ('num', StandardScaler(), ['firedtimes', 'level'])
    ]
)

# Full pipeline with classifier
pipeline = make_pipeline(preprocessor, DecisionTreeClassifier(random_state=42))

# Train the model
pipeline.fit(X, y)

# Prediction function to use in the API
def predict_log(input_json):
    sample = pd.DataFrame([input_json])
    prediction = pipeline.predict(sample)
    return "false positive" if prediction[0] == 1 else "real threat"

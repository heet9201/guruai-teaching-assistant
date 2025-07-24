from setuptools import setup, find_packages

setup(
    name="guruai-teaching-assistant",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Flask==2.0.1",
        "Werkzeug==2.0.3",
        "gunicorn==20.1.0",
        "google-cloud-aiplatform>=1.38.0",
        "vertexai>=0.0.1",
        "google-cloud-storage>=2.14.0",
    ],
    python_requires=">=3.9",
)

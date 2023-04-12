# Introduction

## What is it?

-   Subfield of Artificial Intelligence

-   Systems to automatically learn and improve from experience, without being
    explicitly programmed

-   Algorithms (models) that can interpret and learn from complex data,
    identify patterns, and make predictions or decisions based on it

-   Usage: disease identification, financial projections, image recognition,
    speech recognition, natural language processing, fraud detection, etc.

<figure markdown>
  ![Machine Learning Subfield](./assets/subfield.png){ width="400" }
  <figcaption>Machine Learning Subfield</figcaption>
</figure>

<div style="display: flex; justify-content: center;">
```mermaid
flowchart LR
    subgraph Traditional Programming
        data-->Machine
        rules-->Machine
        Machine-->output
    end
```

```mermaid
flowchart LR
    subgraph Machine Learning
        data-->Machine
        output-->Machine
        Machine-->model
    end
```

</div>

## Types of Machine Learning

There are several machine learning algorithms that enables to build complex models.
These algorithms can be grouped into a certain category depending on its learning process.

-   Supervised Learning: uses labeled data (expected output already known) to train the models.
    The learning process finds the best way to map the inputs to the respective outputs.

-   Unsupervised Learning: uses unlabeled data (doesn't include an output variable) to train the models.
    The model discovers patterns and features in the input data.

-   Semi-Supervised Learning: mix between supervised and unsupervised learning.
    Only some of the ouput is known.

-   Reinforcement Learning: follows trial and error to get the desired result.
    Trains the machine to take the most suitable action at a given moment, and it learns from
    the rewards.

```mermaid
flowchart BT
    A[Supervised Learning]---E[Machine Learning]
    B[Unsupervised Learning]---E[Machine Learning]
    C[Semi-Supervised Learning]---E[Machine Learning]
    D[Reinforcement Learning]---E[Machine Learning]
    F[Classification]---A[Supervised Learning]
    G[Regression]---A[Supervised Learning]
    H[Clustering]---B[Unsupervised Learning]
```

Within the same machine learning, we can also categorize the different problems,
depending on what the machine learning algorithm is trying to predict.

-   Classification: assign class labels to inputs (Ex: classify emails as spam or "not spam")
-   Regression: assign numeric value to inputs (Ex: product price prediction)
-   Clustering: divide input data into clusters (Ex: group together users with same patterns)

<figure markdown>
  ![Classification vs Regression](./assets/classification-vs-regression.png){ width="500" }
    <figcaption>
        Classification and Regression. Adapted from "Regression vs Classification in Machine Learning". 
        Retrieved from [here](https://www.javatpoint.com/regression-vs-classification-in-machine-learning).
    </figcaption>
</figure>

<figure markdown>
  ![Clustering](./assets/clustering.png){ width="500" }
    <figcaption>
        Clustering. Adapted from "Clustering in Machine Learning" by Surya Priy. 
        Retrieved from [here](https://www.geeksforgeeks.org/clustering-in-machine-learning/).
    </figcaption>
</figure>

<figure markdown>
  ![Reinforcement Learning](./assets/reinforcement-learning.png){ width="400" }
    <figcaption>
        Reinforcement. Adapted from "Reinforcement Learning 101" by Shweta Bhatt. 
        Retrieved from [here](https://towardsdatascience.com/reinforcement-learning-101-e24b50e1d292).
    </figcaption>
</figure>

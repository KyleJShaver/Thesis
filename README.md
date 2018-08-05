## Kyle Shaver Thesis
### Minimization of Human Interaction in Supervised Machine Learning Systems

In virtually every machine learning system, a situation can occur wherein an input to the system results in a confidence level too low to act on. When this happens, the system should somehow flag the information it didn't know for further follow up. Sometimes these systems simply log the input and the confidence levels of the results, but there may be more that should be logged. This project strives to find a more effective metric than confidence level alone to denote which inputs would benefit the system most if properly categorized. This metric would then be used by a human to determine which inputs should be manually categorized, prioritizing and, therefore, minimizing the amount of human labor needed to improve the accuracy of the system.

## Instructions to run
1. `cd` into the directory so that `Dockerfile` is in the root
2. `docker build -t kyleshaver/thesis .`
3. `docker run -it -p 8888:8888 -p 6006:6006 -v $(pwd)/bulk:/notebooks/bulk kyleshaver/thesis:latest`
4. Open web browser and navigate to the URL displayed in the terminal, replacing the domain with `localhost`
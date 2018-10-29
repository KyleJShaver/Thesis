import os
import json

propernames = {"baseline": "Baseline",
               "least_represented_letter": "Least Represented Letter",
               "lowest_average": "Lowest Average CI",
               "lowest_letter_confidence": "Lowest Letter CI",
               "random": "Random",
               "unknown_lowest_average": "Unknown Lowest Average CI",
               "unknown_lowest_letter": "Unknown Lowest Letter CI",
               "unknown_random": "Unknown Random"
               }

order = ["baseline", "least_represented_letter", "lowest_average", "lowest_letter_confidence", "random", "unknown_lowest_average", "unknown_lowest_letter", "unknown_random"]

def analyze(filename):
    with open(filename) as results:
        resJSON = json.load(results)
        for batch, trials in resJSON.items():

            averages = dict()
            std_devs = dict()
            perc_improv = dict()
            total_trials = 0

            for trialid, trial in trials.items():

                total_trials += 1

                for approach, incorrect in trial.items():
                    if approach not in propernames:
                        continue

                    if approach not in averages:
                        averages[approach] = 0
                        std_devs[approach] = 0
                        perc_improv[approach] = 0

                    averages[approach] += incorrect
                    perc_improv[approach] += (trial["baseline"] - incorrect) / trial["baseline"]

            print("{}: {} trials".format(batch, total_trials))

            for approach in averages:
                averages[approach] /= total_trials
                perc_improv[approach] /= total_trials

            for trialid, trial in trials.items():
                for approach, incorrect in trial.items():
                    if approach not in propernames:
                        continue

                    std_devs[approach] += pow(incorrect - averages[approach], 2)

            for approach in std_devs:
                std_devs[approach] /= total_trials
                std_devs[approach] = pow(std_devs[approach], 0.5)

            for approach in order:
                print("{}\t{:.2f}\t{:.2f}\t{:.2f}%".format(propernames[approach], averages[approach], std_devs[approach], perc_improv[approach] * 100))

            print("\n\n-------------------------------------------")

analyze("run results.json")
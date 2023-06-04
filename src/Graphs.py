def plot_results(herbivores_counts, predators_counts, plants_counts):
    import matplotlib.pyplot as plt

    time_steps = list(range(len(herbivores_counts)))

    plt.plot(time_steps, herbivores_counts, label="Herbivores", color="blue")
    plt.plot(time_steps, predators_counts, label="Predators", color="red")
    plt.plot(time_steps, plants_counts, label="Plants", color="green")

    plt.xlabel("Time Steps")
    plt.ylabel("Count")
    plt.title("Population Dynamics")
    plt.legend()

    plt.show()
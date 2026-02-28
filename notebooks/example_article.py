from semopy import Model, ModelMeans
from semopy.examples import example_article
from multiprocessing import Process, Queue


def try_fit() -> None:
    data, desc = example_article.get_data(), example_article.get_model()
    m = Model(desc)
    m.fit(data)
    print(m.inspect())


def main():
    for _ in range(10):
        p = Process(target=try_fit)
        p.start()
        p.join()


if __name__ == "__main__":
    main()

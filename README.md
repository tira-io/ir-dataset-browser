# Github Page

Some examples:

- [Topic with high nDCG@10 variange](https://tira-io.github.io/ir-lab-ws-23/topics?topic=5&dataset=ir-lab-jena-leipzig-wise-2023/leipzig-topics-20231025-test)
- [Topic with low nDCG@10 variance](https://tira-io.github.io/ir-lab-ws-23/topics?topic=16&dataset=ir-lab-jena-leipzig-wise-2023/leipzig-topics-20231025-test)
- [Topic with single relevant document retrieved by almost all systems on position 1](https://tira-io.github.io/ir-lab-ws-23/topics?topic=19&dataset=ir-lab-jena-leipzig-wise-2023/leipzig-topics-20231025-test)
- [Browsing some documents](https://tira-io.github.io/ir-lab-ws-23/docs?dataset=ir-lab-jena-leipzig-wise-2023/jena-topics-20231026-test&doc_ids=doc062201800042)
- More examples to come.

Components:

- [Indexing Backend](construct_indices) (test coverage: ![test coverage backend](construct_indices/coverage.svg))
- [UI](ui) (test coverage: ![Coverage of the frontend](ui/coverage/badge-lines.svg))

## Update the datasets

Add new datasets via:

```
./construct_indices/remote_indexes.py
```

```
./construct_indices/construct_topics_for_ui.py
```

## Setup Your Development Environment

We use [devcontainers](https://code.visualstudio.com/docs/devcontainers/containers) for development. To start your environment, either use Github Codespaces (click on "Code" -> "Codespaces" in Github to open one) as the easiest way to get started or [devpod](https://github.com/loft-sh/devpod) as open source alternative (directly pointing to our Kubernetes or your local docker installation).


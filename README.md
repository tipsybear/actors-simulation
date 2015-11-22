[![Stories in Ready](https://badge.waffle.io/tipsybear/actors-simulation.png?label=ready&title=Ready)](https://waffle.io/tipsybear/actors-simulation)
# GVAS Actors Simulation

**A simulation of the Actor model of communication for a variety of applications.**

[![Petros Filipidis actor][theater.jpg]][theater_flickr]

## Getting Started

The simplest way to install the simulator is to use the `setup.py` script included with this repository as follows:

    $ python setup.py install

This will install our simulation library to your Python site-pacakges as well as install a `simulate.py` utility into your path. Of course you can also follow the development instructions below. In order to run the simulation, use the `simulate.py` utility as follows:

    $ simulate.py run <simulation>

Where `<simulation>` is the name of the simulation you'd like to run.

### Configuration

Simulations can be configured either by passing parameters on the command line or through a YAML configuration file. Use `simulate.py run --help` to view the options that can be passed on the command line. In order to create the YAML configuration (the preferred mechanism) copy the `conf/gvas-example.yaml` to one of the following locations:

1. `/etc/gvas.yaml`
2. `$HOME/.gvas.yaml`
3. `$(pwd)/conf/gvas.yaml`

These locations are ordered by priority, e.g. the user `.gvas.yaml` will take priority over the system `/etc/gvas.yaml`. Follow the instructions in the configuration file for modifying configuration values.

## Development

Here are the brief instructions for getting this thing set up for development. First clone the repository and switch directories into it:

    $ git clone git@github.com:tipsybear/actors-simulation.git
    $ cd actors-simulation

Note that you may need to fork this repository on Github into your own repository (and we will definitely accept pull requests). At this point you should set up your virtual environment. If you don't have `virtualenv` and `virtualenvwrapper` installed, please figure out how to set that up and configure it. Create the virtual environment and install the dependencies as follows. With `virtualenvwrapper`:

    $ mkvirtualenv -a $(pwd) -r requirements.txt gvas

And with `virtualenv` alone:

    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt

Create your development configuration by copying the example configuration to the git ignored configuration location:

    (gvas)$ cp conf/gvas-example.yaml conf/gvas.yaml

At this point you should be able to run the tests and have them pass:

    (gvas)$ make test

At this point it's time to switch into the development branch:

    (gvas)$ git checkout origin develop

And you can get started using the contribution details outlined below!

### Contributing

Our Actor Simulation is open source, but because this is a University of Maryland project, we would appreciate it if you would let us know how you intend to use the software (other than simply copying and pasting code so that you can use it in your own projects). If you would like to contribute (especially if you are a student at the University of Maryland), you can do so in the following ways:

1. Add issues or bugs to the bug tracker: [https://github.com/tipsybear/actors-simulation/issues](https://github.com/tipsybear/actors-simulation/issues)
2. Work on a card on the dev board: [https://waffle.io/tipsybear/actors-simulation](https://waffle.io/tipsybear/actors-simulation)
3. Create a pull request in Github: [https://github.com/tipsybear/actors-simulation/pulls](https://github.com/tipsybear/actors-simulation/pulls)

Note that labels in the Github issues are defined in the blog post: [How we use labels on GitHub Issues at Mediocre Laboratories](https://mediocre.com/forum/topics/how-we-use-labels-on-github-issues-at-mediocre-laboratories).

If you are a member of the UMD Tipsy Bear group, you have direct access to the repository, which is set up in a typical production/release/development cycle as described in _[A Successful Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/)_. A typical workflow is as follows:

1. Select a card from the [dev board](https://waffle.io/tipsybear/actors-simulation) - preferably one that is "ready" then move it to "in-progress".

2. Create a branch off of develop called "feature-[feature name]", work and commit into that branch.

        ~$ git checkout -b feature-myfeature develop

3. Once you are done working (and everything is tested) merge your feature into develop.

        ~$ git checkout develop
        ~$ git merge --no-ff feature-myfeature
        ~$ git branch -d feature-myfeature
        ~$ git push origin develop

4. Repeat. Releases will be routinely pushed into master via release branches, then deployed to the server.

Note that pull requests will be reviewed when the Travis-CI tests pass, so including tests with your pull request is ideal!

## About

![Actor Architecture][architecture.png]

An Actor is responsible for all essential elements of a single computation including (1) processing, (2) state, and (3) communication. An analytical job therefore takes the form of a series of actors that accept incoming data, perform processing, and communicate with each other, thereby altering the state of computational space. Because each Actor has its own independent state, an Actor framework or stage can easily instantiate Actors on a variety of nodes and facilitate communication between them, thus abstracting much of the low level details away from the developer.

We propose to develop a proof of concept Actor framework to show that this abstraction is beneficial to developers and will facilitate computations that do require multiple communication streams. A simple, proposed architecture is shown in the figure above. This basic architecture will allow us to develop towards research grade projects including developing an Actor consistency model. In this project, we intend to show the benefits of an actor model by adapting the following applications to Actor space:

1. Timely email analytics data flow
2. Domain decomposition (Lulesh)
3. Book Recommendation using Non-Negative Matrix Factorization

We will measure the performance of the Actor framework including the ability to handle multiple, streaming applications simultaneously as well as its ability to persist and recover from failure. We will also show through a simple user study the benefits and ease of use of the Actor model.


### Attribution

The photo used in this README, [Petros Filipidis actor][theater_flickr] by [Ilias Theodoropoulos](https://www.flickr.com/photos/112615376@N07/) is used under a [CC BY-NC-ND 2.0](https://creativecommons.org/licenses/by-nc-nd/2.0/) creative commons license.

[theater.jpg]: docs/images/theater.jpg
[theater_flickr]: https://flic.kr/p/pKXdHQ
[architecture.png]: docs/images/architecture.png


# RUCS24-Bot Contribution Guide

Welcome to the GitHub repository of the RUCS24 Discord Bot. We appreciate that
you're taking the time to find out how to contribute to improving our bot and, by
proxy, our online community.

The following is a set of guidelines for contributing to RUCS24-Bot, whose source code can be found at [rosalogia/rucs24-bot](https://github.com/rosalogia/rucs24-bot) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

#### Table Of Contents

[Code of Conduct](#code-of-conduct)

[I don't want to read this whole thing, I just have a question!!!](#i-dont-want-to-read-this-whole-thing-i-just-have-a-question)

[What should I know before I get started?](#what-should-i-know-before-i-get-started)
  * [Cog Quickstart](#cog-quickstart)
  * [Style](#style)

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Your First Code Contribution](#your-first-code-contribution)
  * [Pull Requests](#pull-requests)
  * [Git Commit Messages](#git-commit-messages)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [rosalogia@protonmail.ch](mailto:rosalogia@protonmail.ch).

## I don't want to read this whole thing I just have a question!!!

> **Note:** Please don't file an issue to ask a question. You'll get faster results by using the resources below.

RUCS24-Bot is, of course, a discord bot, and questions about its development are best asked in its home:

[RUCS24 Discord Server](https://discord.gg/eYbGFyV)

## What should I know before I get started?

RUCS24-Bot is a Discord bot written in the Python programming language (particularly, Python 3.8). Python is a relatively simple-to-learn and simple-to-use programming language, and yet, it is notably powerful and sees widespread use in the software industry. You're not expected to know Python before contributing, but you should have some programming experience, maybe from a class you took in high school, or some experimentation you've done on your own.

Discord bots are programs that connect to Discord, and provide some sort of functionality that users access through a _bot account_ that they can chat and interact with. Usually Discord bots provide an interface to their functionality through "commands" that users can use in chat.

As an example, a command that connects to Google, searches for some input and returns the first result it finds might be used like this:
```
User A: !google-search discord
Bot Account: First search result leads to the following link: https://discord.com
```
The functionality of a Discord bot is not limited to commands that users may use. Discord bots can watch out for and respond to various "events" that may occur in a Discord server
or within DMs with an individual Discord user. For example, a Discord bot may watch out for new reactions to a particular message, and assign a role to the member who added the reaction in response.

RUCS24-Bot already has some functionality that falls into both categories. If you would like to learn and ask questions about what they are and how they work, feel free to ask them in the RUCS24 Discord server.

Before contributing to RUCS24-Bot, you are encouraged to experiment with the Python programming language and the library that we use to develop applications for Discord in Python, [discord.py](https://discordpy.readthedocs.io/en/latest/). The following resources will be extremely helpful to you in achieving these two things:

* [RUCS24: Setting Up Your Environment Guide](SET_UP.md)
* [RealPython: How to Make a Discord Bot](https://realpython.com/how-to-make-a-discord-bot-python/)

Feel free to ask questions in the server as you prepare yourself to contribute by familiarising yourself with these two things.

#### Cog Quickstart

Within the [discord.py](https://discordpy.readthedocs.io/en/latest/) framework, "cogs" are units of functionality into which a discord bot can easily be divided. Groups of commands or functionalities are grouped together into their own cogs. Within Python, a cog is a class that inherits from `discord.ext.commands.Cog`. If your goal is to add new functionality to the bot, you'll need to add your own cog. Here we will demonstrate the easiest way to get started doing that.

You should first be aware that all cogs are stored in the `cogs/` folder, and that every python file that contains a cog is conventionally named `titlecog.py` where `title` is the title of your cog.

Let's create a cog called `demo`. Start by creating a file called `democog.py` in `cogs/` and put this code inside of it:

```python
from discord.ext import commands

class DemoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # This line in the constructor is required
    
    @commands.command()
    async def test(self, ctx): # the ctx parameter is short for 'context'
        """Sends a message that indicates that the command has worked"""
        await ctx.send("Test succeeded. Command is operational")

def setup(bot):
    bot.add_cog(DemoCog(bot))
``` 
Let's talk briefly about some of the syntax in this example. Some of it may be foreign to you, and that's okay. For example, `async` and `await` are keywords that are rarely touched on in introductory computer science courses. They are constructs that exist to make it easier to write code that does several things at once. That does not mean, however, that you need to or that you should seek to fully understand them right now. In fact, many developers of Python bots do not even have a surface level understanding of these constructs, and have instead simply memorised the correct syntax patterns that will allow them to write bots that work. It may seem strange that this is so common, but there are few repercussions to this in reality.

Similarly, the `@commands.command()` line may also seem foreign to you. This is a _decorator_, a construct in the Python language for engaging in a certain practice known as "metaprogramming." This too is something you need not understand fully or even beyond the surface level in order to write Python bots. When using "cogs" with [discord.py](https://discordpy.readthedocs.io/en/latest/), methods that represent bot commands must have the `@commands.command()` decorator above them, or else they won't register as commands. You may explore this further on your own if you would like, but as with `async` and `await`, understanding this construct fully is neither required nor recommended for beginners.

Finally, the comment between the triple quotes, `"""Sends a message that indicates that the command has worked"""` is a "docstring," Python's built in syntax for documenting how your methods and functions work. When writing a command for RUCS24-Bot, you are _required_ to include docstrings for each command you create. If you fail to do so, your contribution will be rejected until you are able to meet this requirement.

#### Adding the Cog to the Bot

RUCS24-Bot doesn't automatically search for and add every cog in the `cogs/` folder. You will have to edit `main.py` to load the cog.

```python
bot.load_extension("cogs.democog")
```

In the same fashion, you can manually disable any cog that may be causing problems by commenting out the line in `main.py` that loads it.

#### Running the Bot

Run the bot with `python main.py` or whichever command your system uses to execute Python 3 files. If your bot is properly configured according to `example_config.json`, you should find that the bot runs and responds properly when you use the `!test` command in any channel that the bot is able to send messages to.

### Style

There's not a lot to say about style. Stick to [PEP8](https://www.python.org/dev/peps/pep-0008/). If you'd rather not manually learn and conform to PEP8 standards, install a linter for your text editor, or even better, install [`black`](https://pypi.org/project/black/) with `pip`, a Python program that automatically reformats all your code to fit PEP8 standards. Non PEP8 compliant code will be rejected.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for RUCS24-Bot. Following these guidelines helps maintainers and the community understand your report :pencil:, reproduce the behavior :computer: :computer:, and find related reports :mag_right:.

Before creating bug reports, please check [this list](#before-submitting-a-bug-report) as you might find out that you don't need to create one. When you are creating a bug report, please [include as many details as possible](#how-do-i-submit-a-good-bug-report). Fill out [the required template](https://github.com/rosalogia/rucs24-bot/blob/master/.github/ISSUE_TEMPLATE/bug_report.md), the information it asks for helps us resolve issues faster.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### Before Submitting A Bug Report

* **Ask about it in the [Discord](https://discord.gg/eYbGFyV)** so we can help identify whether the problem is on our end.
* **Perform a [cursory search](https://github.com/rosalogia/rucs24-bot/issues?q=is%3Aissue)** to see if the problem has already been reported. If it has **and the issue is still open**, add a comment to the existing issue instead of opening a new one.

#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/). After you've checked in with us in our Discord, create an issue on GitHub and provide the following information by filling in [the template](https://github.com/rosalogia/rucs24-bot/blob/master/.github/ISSUE_TEMPLATE/bug_report.md).

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible. For example, start by explaining how you started RUCS24-Bot, e.g. which command exactly you used in the terminal, or how you started the bot otherwise. When listing steps, **don't just say what you did, but explain how you did it**.
* **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples. If you're providing snippets in the issue, use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **If the problem wasn't triggered by a specific action**, describe what you were doing before the problem happened and share more information using the guidelines below.

Provide more context by answering these questions:

* **Did the problem start happening recently** (e.g. after updating to a new version of RUCS24-Bot) or was this always a problem?
* **Can you reliably reproduce the issue?** If not, provide details about how often the problem happens and under which conditions it normally happens.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for RUCS24-Bot, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion :pencil: and find related suggestions :mag_right:.

Before creating enhancement suggestions, please check [this list](#before-submitting-an-enhancement-suggestion) as you might find out that you don't need to create one. When you are creating an enhancement suggestion, please [include as many details as possible](#how-do-i-submit-a-good-enhancement-suggestion). Fill in [the template](https://github.com/rosalogia/rucs24-bot/blob/master/.github/ISSUE_TEMPLATE/feature_request.md), including the steps that you imagine you would take if the feature you're requesting existed.

#### Before Submitting An Enhancement Suggestion

* **Perform a [cursory search](https://github.com/rosalogia/rucs24-bot/issues?q=is%3Aissue)** to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/). Create an issue on GitHub and provide the following information:

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a clear description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the functionality**.

### Your First Code Contribution

Unsure where to begin contributing to RUCS24-Bot? Here are some steps you can take to get closer to beginning:

1. Read the [Setting Up Your Environment](SET_UP.md) guide and ensure that the bot runs as it exists right now
2. Do the [Quickstart](#cog-quickstart) and ensure that your addition works. Make sure you remove the leftover code from the quickstart before committing to the repository.
3. Check out the following issues to find a place to begin helping

* [Good first issues](https://github.com/rosalogia/rucs24-bot/labels/good%20first%20issue) - issues which should only require a few lines of code, and a test or two.
* [Help wanted issues](https://github.com/rosalogia/rucs24-bot/labels/help%20wanted) - issues which should be a bit more involved than `beginner` issues.

### Pull Requests

Please follow these steps to have your contribution considered by the maintainers:

1. Follow the [style guide](#style)
2. After you submit your pull request, verify that all [status checks](https://help.github.com/articles/about-status-checks/) are passing <details><summary>What if the status checks are failing?</summary>If a status check is failing, and you believe that the failure is unrelated to your change, please leave a comment on the pull request explaining why you believe the failure is unrelated. A maintainer will re-run the status check for you. If we conclude that the failure was a false positive, then we will open an issue to track that problem with our status check suite.</details>

While the prerequisites above must be satisfied prior to having your pull request reviewed, the reviewer(s) may ask you to complete additional design work, tests, or other changes before your pull request can be ultimately accepted.

### Git Commit Messages

We don't care about grammar or anything of the sort, but please actually describe what you're changing or adding in the commit message. Arbitrary commit messages like `Additions`, `Added things`, `Whatever`, `New feature`, etc. will be **promptly** rejected.

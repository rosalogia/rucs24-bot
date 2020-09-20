from discord import Embed
from discord.ext import commands
import json
import requests


class CodeExecutionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.langtable = {
            "csharp": {
                "id": "1",
                "name": "C#",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/8/82/C_Sharp_logo.png",
            },
            "vb": {"id": "2", "name": "Visual Basic .NET", "logo": None},
            "fsharp": {
                "id": "3",
                "name": "F#",
                "logo": "https://fsharp.org/img/logo/fsharp256.png",
            },
            "java": {
                "id": "4",
                "name": "Java",
                "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/3/30/Java_programming_language_logo.svg/262px-Java_programming_language_logo.svg.png",
            },
            "python": {
                "id": "24",
                "name": "Python",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/600px-Python-logo-notext.svg.png",
            },
            "py": {
                "id": "24",
                "name": "Python",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/600px-Python-logo-notext.svg.png",
            },
            "c": {
                "id": "6",
                "name": "C",
                "logo": "https://cdn.iconscout.com/icon/free/png-512/c-programming-569564.png",
            },
            "cpp": {
                "id": "7",
                "name": "C++",
                "logo": "https://raw.githubusercontent.com/isocpp/logos/master/cpp_logo.png",
            },
            "c++": {
                "id": "7",
                "name": "C++",
                "logo": "https://raw.githubusercontent.com/isocpp/logos/master/cpp_logo.png",
            },
            "php": {"id": "8", "name": "PHP", "logo": None},
            "pascal": {"id": "9", "name": "Pascal", "logo": None},
            "objc": {"id": "10", "name": "Objective-C", "logo": None},
            "haskell": {
                "id": "11",
                "name": "Haskell",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Haskell-Logo.svg/200px-Haskell-Logo.svg.png",
            },
            "hs": {
                "id": "11",
                "name": "Haskell",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Haskell-Logo.svg/200px-Haskell-Logo.svg.png",
            },
            "ruby": {
                "id": "12",
                "name": "Ruby",
                "logo": "https://blog.mwpreston.net/wp-content/uploads/2018/09/ruby-logo.png",
            },
            "rb": {
                "id": "12",
                "name": "Ruby",
                "logo": "https://blog.mwpreston.net/wp-content/uploads/2018/09/ruby-logo.png",
            },
            "perl": {"id": "13", "name": "Perl", "logo": None},
            "pl": {"id": "13", "name": "Perl", "logo": None},
            "lua": {
                "id": "14",
                "name": "Lua",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Lua-Logo.svg/200px-Lua-Logo.svg.png",
            },
            "javascript": {
                "id": "23",
                "name": "JavaScript",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Unofficial_JavaScript_logo_2.svg/200px-Unofficial_JavaScript_logo_2.svg.png",
            },
            "js": {
                "id": "23",
                "name": "JavaScript",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Unofficial_JavaScript_logo_2.svg/200px-Unofficial_JavaScript_logo_2.svg.png",
            },
            "lisp": {"id": "18", "name": "Lisp", "logo": None},
            "prolog": {"id": "19", "name": "Prolog", "logo": None},
            "go": {"id": "20", "name": "Go", "logo": None},
            "scala": {"id": "21", "name": "Scala", "logo": None},
            "scheme": {"id": "22", "name": "Scheme", "logo": None},
            "d": {"id": "30", "name": "D", "logo": None},
            "swift": {"id": "37", "name": "Swift", "logo": None},
            "bash": {"id": "38", "name": "Bash", "logo": None},
            "erlang": {"id": "40", "name": "Erlang", "logo": None},
            "erl": {"id": "40", "name": "Erlang", "logo": None},
            "elixir": {"id": "41", "name": "Elixir", "logo": None},
            "ocaml": {
                "id": "42",
                "name": "Ocaml",
                "logo": "https://ocaml.org/logo/Colour/PNG/colour-logo.png",
            },
            "kotlin": {
                "id": "43",
                "name": "Kotlin",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Kotlin-logo.svg/200px-Kotlin-logo.svg.png",
            },
            "kt": {
                "id": "43",
                "name": "Kotlin",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Kotlin-logo.svg/200px-Kotlin-logo.svg.png",
            },
            "brainfuck": {"id": "44", "name": "Brainfuck", "logo": None},
            "fortran": {"id": "45", "name": "Fortran", "logo": None},
            "rust": {
                "id": "46",
                "name": "Rust",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Rust_programming_language_black_logo.svg/1200px-Rust_programming_language_black_logo.svg.png",
            },
            "rs": {
                "id": "46",
                "name": "Rust",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Rust_programming_language_black_logo.svg/1200px-Rust_programming_language_black_logo.svg.png",
            },
            "clojure": {"id": "47", "name": "Clojure", "logo": None},
            "clj": {"id": "47", "name": "Clojure", "logo": None},
        }

    def _exec(self, stdin, language, code, compiler_args=""):
        payload = {
            "LanguageChoice": language,
            "Program": code,
            "Input": stdin,
            "CompilerArgs": compiler_args,
        }

        ereq = requests.post("https://rextester.com/rundotnet/api", data=payload)

        response = ereq.json()

        results = {
            "Warnings": response["Warnings"],
            "Errors": response["Errors"],
            "Result": response["Result"],
            "Stats": response["Stats"],
        }

        return results

    @commands.command()
    async def exec(self, ctx, *, arguments):
        arg_lines = arguments.split("\n")
        language = arg_lines[0].replace("`", "")
        code = "\n".join(arg_lines[1:]).split("```")[0]

        try:
            language_details = self.langtable[language]
        except KeyError:
            await ctx.send(f"**Error**: {language} is not a valid language choice")
            return

        results_embed = Embed()
        results_embed.add_field(
            name="Input:", value=f"```{language}\n{code}```", inline=False
        )

        # Handle any special requirements for languages that have them
        compiler_args = ""

        def replace_identifier(code, replacements):
            lines = code.split("\n")

            for category in replacements.keys():
                for line_number in range(len(lines)):
                    if category in lines[line_number]:
                        line = lines[line_number].split(" ")
                        name_index = line.index(category) + 1
                        line[name_index] = replacements[category]
                        lines[line_number] = " ".join(line)

            return "\n".join(lines)

        if language_details["id"] == "6":
            compiler_args = "-Wall -std=gnu99 -O2 -o a.out source_file.c"
        elif language_details["id"] == "7":
            compiler_args = "-Wall -std=c++14 -O2 -o a.out source_file.cpp"
        elif language_details["id"] == "1":
            code = replace_identifier(
                code, {"namespace": "Rextester", "class": "Program"}
            )
        elif language_details["id"] == "4":
            code = replace_identifier(code, {"class": "Rextester"})
        elif language_details["id"] == "11":
            compiler_args = "-o a.out source_file.hs"

        execution_results = self._exec(
            "", language_details["id"], code, compiler_args=compiler_args
        )

        if (
            execution_results["Errors"] is None
            and execution_results["Result"] is not None
        ):
            result = execution_results["Result"]
            results_embed.add_field(
                name="Output:", value=f"```{result}```", inline=False
            )
            results_embed.color = 0x188F3C
        elif execution_results["Errors"] is not None:
            error = execution_results["Errors"]
            results_embed.add_field(name="Error:", value=f"```{error}```", inline=False)
            results_embed.color = 0xEB0505

        if execution_results["Warnings"] is not None:
            warnings = execution_results["Warnings"]
            results_embed.add_field(
                name="Warnings:", value=f"```{warnings}```", inline=False
            )

        results_embed.add_field(
            name="Stats:", value=execution_results["Stats"], inline=False
        )

        footer_icon = (
            language_details["logo"]
            if language_details["logo"] is not None
            else Embed.Empty
        )

        results_embed.set_footer(
            text=f"{language_details['name']} execution by RexTester",
            icon_url=footer_icon,
        )

        await ctx.send(embed=results_embed)


def setup(bot):
    bot.add_cog(CodeExecutionCog(bot))

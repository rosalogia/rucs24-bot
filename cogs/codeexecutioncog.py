from discord import Embed
from discord.ext import commands
import json
import requests


class CodeExecutionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        tmp_langtable = [
            {
                "id": "1",
                "name": "C#",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/8/82/C_Sharp_logo.png",
                "aliases": {"csharp", "cs"},
            },
            {
                "id": "2",
                "name": "Visual Basic .NET",
                "aliases": {"vbnet", "vb"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/VB.NET_Logo.svg/512px-VB.NET_Logo.svg.png",
            },
            {
                "id": "3",
                "name": "F#",
                "aliases": {"fsharp", "fs"},
                "logo": "https://fsharp.org/img/logo/fsharp256.png",
            },
            {
                "id": "4",
                "name": "Java",
                "aliases": {"java", "jsp"},
                "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/3/30/Java_programming_language_logo.svg/262px-Java_programming_language_logo.svg.png",
            },
            {
                "id": "6",
                "name": "C",
                "aliases": {"c", "h"},
                "logo": "https://cdn.iconscout.com/icon/free/png-512/c-programming-569564.png",
            },
            {
                "id": "7",
                "name": "C++",
                "aliases": {"c++", "h++", "cpp", "hpp", "cc", "hh", "cxx", "hxx"},
                "logo": "https://raw.githubusercontent.com/isocpp/logos/master/cpp_logo.png",
            },
            {
                "id": "8",
                "name": "PHP",
                "aliases": {"php", "php7"},
                "logo": "https://www.freepnglogos.com/uploads/php-logo-png/php-logo-download-proappsoft-blog-12.png",
            },
            {
                "id": "9",
                "name": "Pascal",
                "aliases": {
                    "pascal",
                    "delphi",
                    "dpr",
                    "dfm",
                    "pas",
                    "freepascal",
                    "lazarus",
                    "lpr",
                    "lfm",
                },
                "logo": "https://wiki.freepascal.org/images/0/00/fp32_ico.png",
            },
            {
                "id": "10",
                "name": "Objective-C",
                "aliases": {
                    "objectivec",
                    "mm",
                    "objc",
                    "obj-c",
                    "obj-c++",
                    "objective-c++",
                },
                "logo": "https://raw.githubusercontent.com/librariesio/pictogram/master/vendor/assets/images/objective-c/objective-c.png",
            },
            {
                "id": "11",
                "name": "Haskell",
                "aliases": {"haskell", "hs"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Haskell-Logo.svg/200px-Haskell-Logo.svg.png",
            },
            {
                "id": "12",
                "name": "Ruby",
                "aliases": {"ruby", "rb", "gemspec", "podspec", "thor", "irb"},
                "logo": "https://blog.mwpreston.net/wp-content/uploads/2018/09/ruby-logo.png",
            },
            {
                "id": "13",
                "name": "Perl",
                "aliases": {"perl", "pl", "pm"},
                "logo": "https://www.perlfoundation.org/uploads/1/0/6/6/106663517/powered-by-perl-300px_orig.png",
            },
            {
                "id": "14",
                "name": "Lua",
                "aliases": {"lua"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Lua-Logo.svg/200px-Lua-Logo.svg.png",
            },
            {
                "id": "15",
                "name": "x86 Assembly",
                "aliases": {"x86asm"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Netwide_Assembler.svg/320px-Netwide_Assembler.svg.png",
            },
            {
                "id": "18",
                "name": "Lisp",
                "aliases": {"lisp"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Lisplogo.png/604px-Lisplogo.png",
            },
            {
                "id": "19",
                "name": "Prolog",
                "aliases": {"prolog"},
                "logo": "https://camo.githubusercontent.com/60bbbdf4fe36938bee8b1ead8268a206bc504ee9/687474703a2f2f7777772e7377692d70726f6c6f672e6f72672f69636f6e732f737769706c2e706e67",
            },
            {
                "id": "20",
                "name": "Go",
                "aliases": {"golang", "go"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Go_Logo_Blue.svg/512px-Go_Logo_Blue.svg.png",
            },
            {
                "id": "21",
                "name": "Scala",
                "aliases": {"scala"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Scala-spiral-noise-sm.png",
            },
            {
                "id": "22",
                "name": "Scheme",
                "aliases": {"scheme"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Lambda_lc.svg/375px-Lambda_lc.svg.png",
            },
            {
                "id": "23",
                "name": "JavaScript",
                "aliases": {"javascript", "js", "jsx"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Unofficial_JavaScript_logo_2.svg/200px-Unofficial_JavaScript_logo_2.svg.png",
            },
            {
                "id": "24",
                "name": "Python",
                "aliases": {"python", "py", "gyp"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/600px-Python-logo-notext.svg.png",
            },
            {
                "id": "30",
                "name": "D",
                "aliases": {"d"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/D_Programming_Language_logo.svg/317px-D_Programming_Language_logo.svg.png",
            },
            {
                "id": "32",
                "name": "Tcl",
                "aliases": {"tcl"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Tcl-powered.svg/307px-Tcl-powered.svg.png",
            },
            {
                "id": "37",
                "name": "Swift",
                "aliases": {"swift"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Swift_logo.svg/267px-Swift_logo.svg.png",
            },
            {
                "id": "38",
                "name": "Bash",
                "aliases": {"bash"},
                "logo": "https://raw.githubusercontent.com/odb/official-bash-logo/master/assets/Logos/Icons/PNG/256x256.png",
            },
            {
                "id": "39",
                "name": "Ada",
                "aliases": {"ada"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Ada_Mascot_with_slogan.svg/442px-Ada_Mascot_with_slogan.svg.png",
            },
            {
                "id": "40",
                "name": "Erlang",
                "aliases": {"erlang", "erl"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Erlang_logo.svg/548px-Erlang_logo.svg.png",
            },
            {
                "id": "41",
                "name": "Elixir",
                "aliases": {"elixir"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/9/92/Official_Elixir_logo.png",
            },
            {
                "id": "42",
                "name": "Ocaml",
                "aliases": {"ocaml", "ml"},
                "logo": "https://ocaml.org/logo/Colour/PNG/colour-logo.png",
            },
            {
                "id": "43",
                "name": "Kotlin",
                "aliases": {"kotlin", "kt"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Kotlin-logo.svg/200px-Kotlin-logo.svg.png",
            },
            {
                "id": "44",
                "name": "Brainfuck",
                "aliases": {"brainfuck", "bf"},
                "logo": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/04938ef5-5c6e-4a70-9f5f-cb471a3388df/d9d355y-367661f6-7a3c-479c-a699-8a4ce0d85546.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvMDQ5MzhlZjUtNWM2ZS00YTcwLTlmNWYtY2I0NzFhMzM4OGRmXC9kOWQzNTV5LTM2NzY2MWY2LTdhM2MtNDc5Yy1hNjk5LThhNGNlMGQ4NTU0Ni5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.iYFohy4Ufd-YX1YJ3H5V3mPy3eS4gAHiNufAENXXPdI",
            },
            {
                "id": "45",
                "name": "Fortran",
                "aliases": {"fortran", "f90", "f95"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b6/Fortran.png",
            },
            {
                "id": "46",
                "name": "Rust",
                "aliases": {"rust", "rs"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Rust_programming_language_black_logo.svg/1200px-Rust_programming_language_black_logo.svg.png",
            },
            {
                "id": "47",
                "name": "Clojure",
                "aliases": {"clojure", "clj"},
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Clojure_logo.svg/256px-Clojure_logo.svg.png",
            },
        ]

        self.langtable = dict()

        for lang in tmp_langtable:
            lang_data = lang.copy()
            del lang_data["aliases"]
            for lang_name in lang["aliases"]:
                self.langtable[lang_name] = lang_data

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

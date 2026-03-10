from typing import Any, Callable

from discord.ext import commands

from components.bot import Bot


def is_authorized() -> Callable[..., Any]:
    def predicate(ctx: commands.Context) -> bool:
        if ctx.author.id not in [230778695713947648, 110600636319440896]:
            raise commands.MissingPermissions(["Bot Administrator"])

        return True

    return commands.check(predicate)


class Base(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(name="sync", description="Sync slash commands")
    @is_authorized()
    async def sync(self, ctx: commands.Context) -> None:
        await ctx.defer()

        synced = await self.bot.tree.sync()
        print(synced)
        await ctx.reply("Done!")

    @commands.command(name="reload", description="Reload a cog")
    @is_authorized()
    async def reload(self, ctx: commands.Context, cog: str) -> None:
        await self.bot.reload_extension(f"cogs.{cog}")
        await ctx.reply(f"Reloaded cog: {cog}")

    @commands.command(name="kill", description="Put the bot to sleep")
    @is_authorized()
    async def kill(self, ctx: commands.Context) -> None:
        await ctx.reply("Goodbye!")
        await self.bot.close()


async def setup(bot: Bot) -> None:
    await bot.add_cog(Base(bot))

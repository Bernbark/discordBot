import asyncio
import io
import os
import urllib.request
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageSequence, ImageFont
Image.MAX_IMAGE_PIXELS = 933120000
from src.botUtilities import make_embed
from src.fetchData import fetch_meme, add_meme

# the max size for images returned by the meme generator (to combat Discord 8MB limit)
MAX_SIZE = 800, 600


def thumbnails(frames):
    for frame in frames:
        thumbnail = frame.copy()
        thumbnail.thumbnail(MAX_SIZE, Image.ANTIALIAS)
        yield thumbnail


async def make_meme(extension, ctx, font_mod, caption):
    # open the image/gif
    im = Image.open("in" + extension)

    # we're going to check for the correct size and kill function if too big otherwise OS out of memory occurs
    width, height = im.size
    # print(f"W: {width} H:{height}")
    if width > 5000 or height > 5000:
        await ctx.send("Bro c'mon, this file is too big lolz, the width "
                       "and/or height is too large, so decompression"
                       " would destroy my soft insides.")
        return
    # create the dimensions for the background image, slightly larger thana the picture
    b_width = width + int(width * .03) + 10
    b_height = height + int(height * .25) + 50
    background = Image.new(mode="RGBA", size=(b_width, b_height), color=(0, 0, 0))
    # A list of the frames to be outputted, helps for gifs
    frames = []

    font_size = 1  # starting font size

    # portion of image width you want text width to be
    img_fraction = 0.50

    font = ImageFont.truetype(font="Memesique-Regular.ttf", size=font_size)
    while font.getsize(caption)[0] < img_fraction * im.size[0]:
        # iterate until the text size is just larger than the criteria
        font_size += 1
        font = ImageFont.truetype(font="Memesique-Regular.ttf", size=font_size)

    # optionally de-increment to be sure it is less than criteria
    font_size -= 1
    # allow user to adjust final font size
    font_size *= font_mod
    caption_parts = []
    """
    All we're doing here is trying to split the meme's caption up a little more so that it doesn't make one 
    continuous line of text, and also help it look more structured and fit into the image
    """
    if len(caption) > 22:
        words = caption.split(' ')
        line_break = 4
        i = 1
        if len(words) > 1:
            # adding new line whenever i == line_break (the number of words we want per line)
            for word in words:
                if "." in word or i == line_break:
                    caption_parts.append(word.strip('\n') + "\n")
                    i = 0
                else:
                    caption_parts.append(word.strip('\n') + " ")
                i += 1
            print(f"{caption_parts}")
            caption = ''.join(caption_parts)
        # I noticed the font becomes too small on larger fonts, this is just a hacky fix
        font_size *= 3
    # the font should be done being manipulated by now
    font = ImageFont.truetype(font="Memesique-Regular.ttf", size=int(font_size))
    stroke_color = "#000000"
    # for now, we're just taking a single frame and converting it to a jpeg, in the future, probably make into GIF
    if extension.lower() == ".webp":
        im = Image.open("in" + extension).convert("RGB")
        #extension = ".jpg"
        #im.save("in" + extension, "jpeg")
    # Loop over each frame in the animated image
        for frame in ImageSequence.Iterator(im):
            background = Image.new(mode="RGB", size=(b_width, b_height), color=(0, 0, 0))
            frame = frame.convert("RGBA")
            background.paste(frame, (10, 10))
            # Draw the text on the frame
            d = ImageDraw.Draw(background)
            d.text((10, b_height - int(b_height * .2)), f"{caption}", font=font, stroke_width=2,
                   stroke_fill=stroke_color)
            del d

            # However, 'frame' is still the animated image with many frames
            # It has simply been seeked to a later frame
            # For our list of frames, we only want the current frame

            # Saving the image without 'save_all' will turn it into a single frame image, and we can then re-open it
            # To be efficient, we will save it to a stream, rather than to file
            b = io.BytesIO()

            background.save(b, format="WEBP")
            background = Image.open(b)

            # Then append the single frame image to a list of frames
            frames.append(background)
        frames[0].save('out' + extension)
    elif extension.lower() == ".gif":

        for frame in ImageSequence.Iterator(im):
            frame = frame.convert("RGBA")
            background = Image.new(mode="RGBA", size=(b_width, b_height), color=(0, 0, 0))
            background.paste(frame, (10, 10), mask=frame)
            # Draw the text on the frame
            d = ImageDraw.Draw(background)

            d.text((10, b_height - int(b_height * .2)), f"{caption}", font=font,
                   stroke_width=2, stroke_fill=stroke_color)
            del d

            # However, 'frame' is still the animated image with many frames
            # It has simply been seeked to a later frame
            # For our list of frames, we only want the current frame

            # Saving the image without 'save_all' will turn it into a single frame image, and we can then re-open it
            # To be efficient, we will save it to a stream, rather than to file
            b = io.BytesIO()

            background.save(b, format="GIF", optimize=True, quality=10)
            background = Image.open(b)

            frames.append(background)

        # Save the frames as a new image
        frames = thumbnails(frames)
        om = next(frames)
        om.info = im.info
        om.save('out' + extension, save_all=True, append_images=list(frames), loop=0)

    elif extension.lower() == ".jpg" or extension.lower() == ".jpeg":
        """# im = Image.open("in"+extension)
        image_draw = ImageDraw.Draw(im)
        image_draw.text((10, 100), f"{caption}", font=font)
        b = io.BytesIO()

        image = Image.open(b)
        image.save(b, format="JPEG")
        image.save('out' + extension)
        picture = discord.File("out" + extension)
        await ctx.message.delete()
        await ctx.send(file=picture)"""
        for frame in ImageSequence.Iterator(im):
            background = Image.new(mode="RGB", size=(b_width, b_height), color=(0, 0, 0))
            frame = frame.convert("RGBA")
            background.paste(frame, (10, 10))
            # Draw the text on the frame
            d = ImageDraw.Draw(background)
            d.text((10, b_height - int(b_height * .2)), f"{caption}", font=font, stroke_width=2,
                   stroke_fill=stroke_color)
            del d

            # However, 'frame' is still the animated image with many frames
            # It has simply been seeked to a later frame
            # For our list of frames, we only want the current frame

            # Saving the image without 'save_all' will turn it into a single frame image, and we can then re-open it
            # To be efficient, we will save it to a stream, rather than to file
            b = io.BytesIO()

            background.save(b, format="JPEG")
            background = Image.open(b)

            # Then append the single frame image to a list of frames
            frames.append(background)
        frames[0].save('out' + extension)
    elif extension.lower() == ".png":
        for frame in ImageSequence.Iterator(im):
            background = Image.new(mode="RGB", size=(b_width, b_height), color=(0, 0, 0))
            frame = frame.convert("RGBA")
            background.paste(frame, (10, 10))
            # Draw the text on the frame
            d = ImageDraw.Draw(background)
            d.text((10, b_height - int(b_height * .2)), f"{caption}", font=font, stroke_width=2,
                   stroke_fill=stroke_color)
            del d

            # However, 'frame' is still the animated image with many frames
            # It has simply been seeked to a later frame
            # For our list of frames, we only want the current frame

            # Saving the image without 'save_all' will turn it into a single frame image, and we can then re-open it
            # To be efficient, we will save it to a stream, rather than to file
            b = io.BytesIO()

            background.save(b, format="PNG")
            background = Image.open(b)

            # Then append the single frame image to a list of frames
            frames.append(background)
        frames[0].save('out' + extension)

class Memes(commands.Cog):
    """
    The place where all meme related functions are held. This is where the Memedex functions and the meme generator
    functions reside.
    """
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.acceptedGenres = [
            "confused",
            "happy",
            "sad",
            "test",
        ]

    @commands.cooldown(3, 120, commands.BucketType.user)
    @commands.command(
        name="memeitize",
        aliases=["memetize","m"],
        help="Add words to a picture"
    )
    async def memeitize(self, ctx: commands.Context, url: str = None, caption: str = None, font_mod: float = 1):
        """
        This is custom meme generator. Currently it takes in a caption, a picture/gif, and an optional font size
        modifier. It then creates a black background slightly wider and taller than the image/images and paste the image
        to the background, along with the caption somewhere around the bottom, hopefully not overlapping too much.

        This function is really picky, and doesn't always work great, but with the font size mod people can try to at
        least fit all of their text
        :param ctx: discord Context
        :param url: image URL
        :param caption: user given meme caption
        :param font_mod: a multiplier on the final font size
        :return: Nothing
        """
        if len(ctx.message.attachments) > 0:
            filename = ctx.message.attachments[0].filename
            print(filename)
            name, extension = os.path.splitext(filename)
            print(extension)
            file_bytes = await ctx.message.attachments[0].save("in"+extension)  # saves the file

            await make_meme(extension, ctx, font_mod, caption)
            await asyncio.sleep(3)
            picture = discord.File("out" + extension)
            await ctx.message.delete()
            await ctx.send(file=picture)
            return
        # require these from the user, otherwise the whole process won't work
        if url is None or caption is None:
            await ctx.send("Please provide a URL and caption for the meme generator")
        # we're getting the extension so we can tell what to save this as, and how pillow should treat the images
        name, extension = os.path.splitext(url)
        # discord won't let us access the images once they're already on their server
        if "discordapp" in name:
            await ctx.send("Unfortunately I can't access images from discordapp attachments :( Try another URL")
        # find the picture online and save it by in.extension_name
        urllib.request.urlretrieve(f"{url}","in"+extension)
        # let's us not work with crazy sized files
        file_size_in_bytes = os.stat("in"+extension).st_size
        # if greaater than 10MB kill the function
        if file_size_in_bytes > 10120000:
            await ctx.send("Bro c'mon, this file is too big lolz, try something under 10 MB")
            return
        await make_meme(extension,ctx,font_mod,caption)
        picture = discord.File("out" + extension)
        await ctx.message.delete()
        await ctx.send(file=picture)

    @commands.cooldown(4, 10, commands.BucketType.user)
    @commands.command(
        name="meme",
        help="Generate a meme from one of the meme genres."
    )
    async def meme(self, ctx: commands.Context, genre: str = ""):
        """
        We call on fetch_meme from fetchData.py which allows us to connect to the memedex and get a random meme based on
        genre
        :param ctx:
        :param genre:
        :return:
        """
        meme = await fetch_meme(self.bot, genre)
        await ctx.send(content=meme["_id"])

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.command(
        name="addmeme",
        help="Add a meme by giving it a genre and an image url (copy image address/location and paste)."
    )
    async def add_new_meme(self, ctx: commands.Context, genre: str = "", url: str = None):
        """
        Allows users to try to add new memes to the memedex. The user has to input a genre and then the url of the
        image/gif.

        The program waits for a few seconds and checks to see if this given url presents an embed with an image.
        It isn't the best check ever, but I've tried to prevent random websites and links from being allowed.
        Once accepted, the url is added to the memedex with its associated genre.
        :param ctx:
        :param genre:
        :param url:
        :return:
        """
        await asyncio.sleep(6)
        msg = ctx.message

        if len(msg.embeds) == 0:
            embed = make_embed("This won't be accepted as an image/gif")
            await ctx.send(embed=embed)
            return
        if url is None:
            embed = make_embed("You didn't enter an image url")
            await ctx.send(embed=embed)
            return
        if genre == "":
            embed = make_embed("You need to choose a genre for this meme to be referenced by.")
            await ctx.send(embed=embed)
            return
        if genre not in self.acceptedGenres:
            embed = make_embed(f"You need to choose a genre from this list: {self.acceptedGenres}")
            await ctx.send(embed=embed)
            return
        name, extension = os.path.splitext(url)
        notAllowedExt = [".io", ".com", ".org", ".gov", ".io/", ""]

        if extension in notAllowedExt:
            embed = make_embed(f"You need to use a real image, preferably from an online source.")
            await ctx.send(embed=embed)
            return
        try:
            await add_meme(self.bot, genre, url)
            embed = make_embed("Oh boy, a new meme added!")
            await ctx.send(embed=embed)
        except:
            embed = make_embed("This meme has probably already been added to the Memedex")
            await ctx.send(embed=embed)

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.command(
        name="memetypes",
        help="Show which genres of memes you can upload to the bot."
    )
    async def meme_types(self, ctx: commands.Context):
        """
        Shows the user which meme genres they can call on from the memedex.
        :param ctx:
        :return:
        """
        embed = make_embed("Allowed types for adding:", f"{self.acceptedGenres}")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):

    await bot.add_cog(
        Memes(bot)
    )


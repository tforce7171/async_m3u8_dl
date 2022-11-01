import async_m3u8_dl
import click

@click.command()
@click.option('-i', type=str, required=True, help='input m3u8 filepath/url')
@click.argument('output', type=str, required=True)

def main(i, output):
    print("a")
    async_m3u8_dl.download(i, output)

if __name__ == '__main__':
    main()
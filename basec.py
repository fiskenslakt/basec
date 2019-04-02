import base64

import click


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.option('--from', '-f', 'orig', flag_value='from', help='Convert from base64 encoded string')
@click.option('--to', '-t', 'orig', flag_value='to', help='Convert to base64 encoded string')
@click.option('--url', '-u', is_flag=True, help='Use url-safe alternative characters (hyphen and underscore)')
@click.argument('convert', nargs=-1, required=True)
def b64(orig, url, convert):
    """Convert to or from base64 encoded string."""
    altchars = b'-_' if url else None

    if orig == 'from':
        convert = bytes(convert[0], encoding='utf-8')
        decoded = base64.b64decode(convert, altchars=altchars)
        click.echo(decoded)
    elif orig == 'to':
        convert = bytes(' '.join(convert), encoding='utf-8')
        encoded = base64.b64encode(convert, altchars=altchars)
        click.echo(encoded)


@cli.command(name='hex')
@click.option('--from', '-f', 'orig', flag_value='from', help='Convert from hexadecimal to decimal')
@click.option('--to', '-t', 'orig', flag_value='to', help='Convert to hexadecimal from decimal')
@click.argument('convert', nargs=-1, required=True)
def hexadecimal(orig, convert):
    """Convert to or from hexadecimal."""
    if orig == 'from':
        decimal = [int(i, 16) for i in convert]
        click.echo(' '.join(str(d) for d in decimal))
    elif orig == 'to':
        hex_ = [hex(int(i)) for i in convert]
        click.echo(' '.join(hex_))


@cli.command(name='bin')
@click.option('--from', '-f', 'orig', flag_value='from', help='Convert binary number(s) to decimal or text')
@click.option('--to', '-t', 'orig', flag_value='to', help='Convert number or text to binary')
@click.option('--text/--num', '-T/-n', default=False, help='Type to convert from or to (default is num)')
@click.option('--no-space', '-S', is_flag=True, help='Indicate the string of bytes has no spaces between each byte')
@click.argument('convert', nargs=-1, required=True)
def binary(orig, text, no_space, convert):
    """Convert to or from a binary number."""
    if orig == 'from':
        if no_space:
            if len(convert) > 1:
                raise click.BadArgumentUsage(f'Expected one argument with --no-space flag, got {len(convert)}')

            # parse long string of bits
            # into multiple bytes
            bits = convert[0]
            bytes_ = [bits[i:i+8] for i in range(0, len(bits), 8)]
        else:
            # supports more than 8 bits per item in convert
            # despite the name
            bytes_ = convert

        # binary to text
        if text:
            # get decimal representation for each byte
            # then convert each decimal to a character
            # raise error if number can't be converted
            decimal = [int(byte, 2) for byte in bytes_]

            try:
                text = ''.join(map(chr, decimal))
            except (ValueError, OverflowError):
                raise click.BadArgumentUsage('Number too large to convert to text')

            click.echo(text)
        # binary to decimal
        else:
            # get decimal representation of each "byte"
            # casted to a string
            decimal = [str(int(byte, 2)) for byte in bytes_]
            click.echo(' '.join(decimal))

    elif orig == 'to':
        # text to binary
        if text:
            # get ordinal for each character in string
            decimal = [ord(c) for c in ' '.join(convert)]

            if no_space and any(n > 255 for n in decimal):
                raise click.BadOptionUsage(
                    'no_space',
                    'One or more characters require more than 8 bits, cannot use --no-space flag'
                    )

            # use format() for conversion and 0 padding
            bytes_ = [format(n, '08b') for n in decimal]

            if no_space:
                click.echo(''.join(bytes_))
            else:
                click.echo(' '.join(bytes_))

        # decimal to binary
        else:
            # convert each decimal number to binary
            try:
                binary = [bin(int(n))[2:] for n in convert]
            except ValueError:
                raise click.BadArgumentUsage('Must provide a number')
            click.echo(' '.join(binary))


if __name__ == '__main__':
    cli()

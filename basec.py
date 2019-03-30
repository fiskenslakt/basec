import click


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command(name='bin')
@click.option('--from', '-f', 'orig', flag_value='from', help='Convert binary number(s) to decimal')
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
            decimal = [int(byte,2) for byte in bytes_]
            text = ''.join(map(chr, decimal))
            click.echo(text)
        # binary to decimal
        else:
            # get decimal representation of each "byte"
            # casted to a string
            decimal = [str(int(byte,2)) for byte in bytes_]
            click.echo(' '.join(decimal))

    elif orig == 'to':
        # text to binary
        if text:
            # get ordinal for each character in string
            # then convert each character to binary
            decimal = map(ord, ' '.join(convert))
            bytes_ = [bin(n)[2:] for n in decimal]
            if no_space:
                click.echo(''.join(bytes_))
            else:
                click.echo(' '.join(bytes_))
        # decimal to binary
        else:
            # convert each decimal number to binary
            binary = [bin(int(n))[2:] for n in convert]
            click.echo(' '.join(binary))


if __name__ == '__main__':
    cli()

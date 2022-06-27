"""Console script for otel_python_cli."""
import sys
import click

from opentelemetry.sdk.trace.id_generator import RandomIdGenerator

from .otel import create_span, create_counter
from .utils import parse_attributes


@click.group()
def main(args=None):
    pass  # pragma: no cover


@main.group()
def generate():
    pass  # pragma: no cover


@generate.command(name="trace_id")
@click.option(
    "-d", "--decimal", is_flag=True, default=False, help="Print in decimal base"
)
def generate_trace_id(decimal):
    trace_id = RandomIdGenerator().generate_trace_id()
    if decimal:
        click.echo(trace_id)
    else:
        click.echo(f"{trace_id:x}")


@generate.command(name="span_id")
@click.option(
    "-d", "--decimal", is_flag=True, default=False, help="Print in decimal base"
)
def generate_span_id(decimal):
    span_id = RandomIdGenerator().generate_span_id()
    if decimal:
        click.echo(span_id)
    else:
        click.echo(f"{span_id:x}")


@main.command()
@click.argument("span_name")
@click.option("-s", "--service", default="otel-cli-python")
@click.option(
    "--start", type=int, help="Span start time in nanoseconds since the epoch"
)
@click.option("--end", type=int, help="Span end time in nanoseconds since the epoch")
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Print spans to stdout"
)
@click.option("--tp", "--traceparent", help="Trace parent")
@click.option("--span-id", help="Manually set span ID")
@click.option("--trace-id", help="Manually set trace ID")
@click.option(
    "-a",
    "--attribute",
    multiple=True,
    help="Attributes in the format 'key=value'. "
    "For multiple attributes use -a 'key1=val' -a 'key2=val'",
)
@click.option("--status", type=click.Choice(["UNSET", "OK", "ERROR"]), default="UNSET")
@click.option("--message")
def span(span_name, **kwargs):
    # Parse attribute to dict
    attributes = dict([attr.split("=", 1) for attr in kwargs["attribute"]])
    myspan = create_span(
        span_name,
        service_name=kwargs["service"],
        start_time=kwargs["start"],
        end_time=kwargs["end"],
        traceparent=kwargs["tp"],
        span_id=kwargs["span_id"],
        trace_id=kwargs["trace_id"],
        attributes=attributes,
        status_code=kwargs["status"],
        status_message=kwargs["message"],
    )
    if kwargs["verbose"]:
        print(myspan.to_json())


@main.group()
def metric():
    pass  # pragma: no cover


@metric.command()
@click.argument("counter_name")
@click.argument("amount", type=int, default=1)
@click.option(
    "-a",
    "--attribute",
    multiple=True,
    help="Attributes in the format 'key=value'. "
    "For multiple attributes use -a 'key1=val' -a 'key2=val'"
    "Attributes are strings by default. To convert to other types, use these prefixes:"
    "  'int:' -> Convert to a number (e.g. int:key=100)"
    "  'float:' -> Convert to a float (e.g. float:key=0.1)",
)
def counter(**kwargs):
    # Parse attribute to dict
    attributes = parse_attributes(kwargs["attribute"])
    create_counter(
        kwargs.get("counter_name"), kwargs.get("amount"), attributes=attributes
    )


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

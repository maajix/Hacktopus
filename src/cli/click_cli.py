import click
from src.flow.builder import FlowBuilder


def parse_to_dict(ctx) -> dict:
    # Parse provided arguments into a dict
    provided_args = {}
    i = 0
    while i < len(ctx.args):
        arg = ctx.args[i]
        if arg.startswith('--'):
            arg_name = arg[2:]  # Remove --
            if i + 1 < len(ctx.args) and not ctx.args[i + 1].startswith('--'):
                provided_args[arg_name] = ctx.args[i + 1]
                i += 2
            else:
                provided_args[arg_name] = True
                i += 1
        else:
            i += 1
    return provided_args


def collect_missing(required_vars, provided_args) -> dict:
    # Collect missing variables interactively
    final_args = {}
    for var in required_vars:
        if var in provided_args:
            final_args[var] = provided_args[var]
        else:
            # Prompt for missing variable
            value = click.prompt(f"Enter a value for variable '{var}'", type=str)
            final_args[var] = value

    return final_args


def check_unknown(ctx, required_vars, provided_args) -> set:
    # Validate no unknown arguments were provided
    unknown_args = set(provided_args.keys()) - set(required_vars)
    if unknown_args:
        click.echo(f"Warning: Unknown arguments provided: {', '.join(unknown_args)}")
        if not click.confirm("Do you want to continue?"):
            ctx.exit(1)

    return unknown_args


@click.group()
def cli():
    """Flow execution CLI tool."""
    pass


@cli.group()
def flow():
    """Flow management commands."""
    pass


class FlowRunCommand(click.Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Allow unknown options to be passed
        self.allow_extra_args = True
        self.ignore_unknown_options = True


@flow.command(cls=FlowRunCommand)
@click.argument('flowname')
@click.pass_context
def run(ctx, flowname: str):
    """
    Run a specific flow with dynamic arguments.

    Args:
        flowname: Name of the flow to run
        :param flowname: flowname to execute without extension
        :param ctx: click context
    """

    try:
        from rich import print as rp

        # Load required variables from flow
        loaded_flow = FlowBuilder(filename=f"{flowname}.yaml")
        required_vars = loaded_flow.variables

        provided_args = parse_to_dict(ctx)
        final_args = collect_missing(required_vars, provided_args)

        check_unknown(ctx, required_vars, provided_args)

        # Execute flow with collected arguments
        click.echo(f"\nRunning flow '{flowname}' with parameters:")
        for arg, value in final_args.items():
            click.echo(f"  {arg}: {value}")

        loaded_flow.replace_variables_with(final_args)
        rp(loaded_flow.parsed_flow_data)

    except Exception as e:
        click.echo(f"Error running flow: {str(e)}", err=True)
        ctx.exit(1)

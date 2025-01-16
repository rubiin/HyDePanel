import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-g', '--generate-config', help='Generate a configuration file', action='store_true')
parser.add_argument('-c', '--config', help='Path to the configuration file', type=str, default='config.json')
parser.add_argument('-q', '--quiet', help='Disable all logging', action='store_true')
parser.add_argument('-r', '--run', help='Run the application', action='store_true')
args = parser.parse_args()

if args.generate_config:
    from utils.config import generate_config

    generate_config()
    exit()
elif args.run:
    app
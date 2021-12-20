import dataFunc
import argparse


parser = argparse.ArgumentParser(description="Data generation")
parser.add_argument('-o', '--output', help='Output file name', required=True)
parser.add_argument('-s', '--size', default=1024, help="File size in kB. Default: 1 kB")
parser.add_argument('-l', '--laplace', action='store_true', help="Laplace distribution. Default: Uniform")
parser.add_argument('-n', '--normal', action='store_true', help="Normal distribution. Default: Uniform")



args = parser.parse_args()


size = int(args.size) * 1024
generator = None

if args.normal:
    generator = dataFunc.gen_normal

elif args.laplace:
    generator = dataFunc.gen_laplace

else:
    generator = dataFunc.gen_uniform

data = generator(size)

data = dataFunc.normalize(data)
data = dataFunc.convert_to_string(data)
dataFunc.write_to_file(args.output, data)


from arch.baseline import Baseline
from util.training import make_training_parser, main


if __name__ == "__main__":
    parser = make_training_parser()
    args = parser.parse_args()
    model = Baseline(7, args.hidden_dim, 2).cuda()
    main(args, model)

def main():
    import argparse
    import json
    from .dvidsync import sync
    
    parser = argparse.ArgumentParser()
    parser.add_argument("configfile")
    args = parser.parse_args()
    fin = open(args.configfile)
    config = json.load(fin)
    
    # run config
    sync(config)
    

if __name__ == "__main__":
    main()



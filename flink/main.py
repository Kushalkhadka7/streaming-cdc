from pyflink.datastream import StreamExecutionEnvironment

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    ds = env.from_collection([1, 2, 3, 4])
    ds.print()
    env.execute("PyFlink Job")

if __name__ == "__main__":
    main()
from hartrix_base_cli import __main__ as hartrix
import os,sys,asyncio
if __name__=="__main__":
    path=os.path.abspath(os.path.dirname(__file__))
    sys.exit(
        asyncio.run(
            hartrix.main(
                prefix=path,
                data=os.path.join(path,"data"),
                args=sys.argv
            )
        )
    )
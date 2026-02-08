from hartrix_base_cli import __main__ as hartrix
import os,sys
if __name__=="__main__":
    path=os.path.abspath(os.path.dirname(__file__))
    sys.exit(
        hartrix.main(
            prefix=path,
            data=os.path.join(path,"data"),
            args=sys.argv
        )
    )
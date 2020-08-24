import pickle
from pathlib import Path
from typing import Tuple

import fire
import pandas as pd

from scipy.spatial import KDTree


def main():
    fire.Fire(calc)


def calc(arg1: str, arg2: str = ""):
    """住所⇔座標

    :param arg1: 住所または緯度
    :param arg2: arg1が緯度の場合に経度, defaults to ""
    """
    sg = Geocoding()
    if arg2:
        print(sg.addr(float(arg1), float(arg2)))
    else:
        print(sg.point(arg1))


class Geocoding:
    data_path = Path(__file__).parent / "data.pkl"
    address = None
    kd_tree = None
    addr2pt = None

    def __init__(self, csv: str = ""):
        if self.address is None:
            if self.data_path.is_file():
                with open(self.data_path, "rb") as fp:
                    res = pickle.load(fp)
            else:
                res = make_data(csv)
                with open(self.data_path, "wb") as fp:
                    pickle.dump(res, fp)
            Geocoding.address, Geocoding.kd_tree, Geocoding.addr2pt = res

    def addr(self, lati: float, lngi: float) -> str:
        return self.address[self.kd_tree.query((lati, lngi))[1]]

    def point(self, addr: str) -> Tuple[float, float]:
        return self.addr2pt.get(addr)


def make_data(csv, encoding="utf-8", lati="緯度", lngi="経度", addr="都道府県名 市区町村名 大字町丁目名"):
    df = pd.read_csv(csv, encoding=encoding)
    for c in [lati, lngi]:
        df[c] = df[c].round(6)
    df["addr_"] = eval("+".join(f"df['{c}']" for c in addr.split()))
    df.drop_duplicates("addr_", inplace=True)  # 同一住所は最初の座標とする
    df["point_"] = list(map(tuple, df[[lati, lngi]].values))
    kd_tree = KDTree(df.point_.to_list())
    addr2pt = df.set_index("addr_").point_.to_dict()
    return df.addr_.to_list(), kd_tree, addr2pt

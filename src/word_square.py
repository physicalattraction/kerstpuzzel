def transpose():
    return '\n'.join([''.join(row[index] for row in split_square)
                      for index in range(nr_cols)])


square = """BENESRTSKTAEPSMTTAWP
ZZEOGECKEDIEPTNWSEME
DDEEDSTTHAUPENABLKKE
SOPRAUTUAODEIUXBIIEO
EOVXPAILOSTAPEOOLWOP
GFTXEUKFIUOEZWAUEAAW
IOEOKUEUODYWAAOLEKBE
GGAUPVUAWMDIIXAEOAIK
EGAIUEPHEEIEHQHEAOKT
BNAUAVEEUEXSEDUEEOJE
!SFOUEANOEBFUUHEIRUA
HDDSOISEHTEESIKOAAJA
IOUENUBUAATIPXPSNUKU
ZTIOEKUIVFBEDIKAEOIX
EFXOAEOGQEAVEIHINUUO
IKOISETRURYCVEIAEOTT
CAFUIOTLUEIEEKOIUPKJ
LEOTEIWTHOHKTUUWUWEA
WIPKOICKOUOIKBAPEIAR
URWESUIEBDDUAJEIIUGE
WEIOEOAWRUMDUCNAOAEB
SEOJEEEEOXSASAOGDULT
IOF                 """
text = square.replace('\n', '')
split_square = square.split('\n')
nr_rows = len(split_square)
nr_cols = len(split_square[0])
transpose_square = transpose()
transpose_text = transpose_square.replace('\n', '')
transpose_split_square = transpose_square.split('\n')


def every_nth_letter(n: int):
    for start_letter in range(n):
        print(text[start_letter::n])
        print(transpose_text[start_letter::n])


if __name__ == '__main__':
    for i in range(2, 10):
        every_nth_letter(i)

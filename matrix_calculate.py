import sys
import tkinter as tk

sys.setrecursionlimit(3000)

class Matrix:
    def __init__(self, data):
        self._data = data
    def __add__(self, other):
        return Matrix([[x + y for x, y in zip(z1, z2)]  for z1, z2 in zip(self._data, other._data)])
    __iadd__ = __add__
    def __sub__(self, other):
        return Matrix([[x - y for x, y in zip(z1, z2)] for z1, z2 in zip(self._data, other._data)])
    __isub__ = __sub__
    def __mul__(self, other):
        if isinstance(other, Matrix):
            s_data, o_data = self._data, other._data
            result = []
            for r in range(len(s_data)):
                row = []
                for c in range(len(o_data[0])):
                    sum = 0
                    for  m in range(len(s_data[0])):
                        sum += s_data[r][m] * o_data[m][c]
                    row.append(sum)
                result.append(row)
            return Matrix(result)

        elif isinstance(other, (int, float)):
            return Matrix([[x * other for x in r] for r in self._data])
    __rmul__ = __imul__ = __mul__
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Matrix([[x / other for x in r] for r in self._data])
    def __matmul__(self, other):
        return self.__mul__(other)
    __rmatmul__ = __imatmul__ = __matmul__
    def __str__(self):
        longest, data = 0, self._data
        for r in data:
            for c in r:
                length = len(str(c))
                if length > longest:
                    longest = length
        result = ""
        for r in data:
            text = ""
            for c in range(len(r)):
                text += f"{r[c]:{longest+(2 if c != 0 else 0)}n}"
            result += "[" + text + "]\n"
        return result.rstrip()
        

    def __iter__(self):
        for r in self._data:
            yield r

    def transpose(self):
        return Matrix(list(map(list, zip(*self._data))))

    @staticmethod
    def transpose_static(data):
        return Matrix(list(map(list, zip(*data))))

    @property
    def size(self):
        return (len(self._data), len(self._data[0]))

    def is_square_matrix(self):
        return len(self._data) == len(self._data[0])
     
    def determinant(self):
        data, size = self._data, self.size
        if size[0] == 1:return data[0][0]
        elif size[0] == 2:return data[0][0] * data[1][1] - data[0][1] * data[1][0]
        elif size[0] == 3:
            result = 0
            for p in range(3):
                u, n = 1, 1
                for r in range(3):
                    u *= data[r][(r+p)%3]
                    n *= data[r][-((1+r+p)%3)]
                result += u - n
            return result
        else:
            result = 0
            for c in range(size[1]):
                result += data[0][c] * self.cofactor((1, c+1))
            return result 


    @staticmethod
    def determinant_static(data):
        size = (len(data), len(data[0]))
        if size[0] == 1:return data[0][0]
        elif size[0] == 2:return data[0][0] * data[1][1] - data[0][1] * data[1][0]
        elif size[0] == 3:
            result = 0
            for p in range(3):
                u, n = 1, 1
                for r in range(3):
                    u *= data[r][(r+p)%3]
                    n *= data[r][-((1+r+p)%3)]
                result += u - n
            return result
        else:
            result = 0
            for c in range(size[1]):
                result += data[0][c] * Matrix.cofactor_static(data, (1, c+1))
            return result

    def inverse(self):
        if self.determinant():
            data, size = self._data, self.size
            if size[0] == 1:
                return Matrix([[1 / data[0][0]]]) 
            elif size[0] == 2:
                det = self.determinant()
                return Matrix([[data[1][1]/det, -data[0][1]/det], [-data[1][0]/det, data[0][0]/det]])
            else:
                det = self.determinant()
                return self.adjoint() / det

    def minor(self, position):
        data, size, position = self._data, self.size[0], tuple(map(lambda x: x - 1, position))
        if size == 1: return 0
        else:
            cut = []
            for r in range(size):
                row = []
                for c in range(size):
                    if r != position[0] and c != position[1]:
                        row.append(data[r][c])
                if row: cut.append(row)
            return Matrix.determinant_static(cut)

    @staticmethod
    def minor_static(data, position):
        size, position = len(data), tuple(map(lambda x: x - 1, position))
        if size == 1: return 0
        else:
            cut = []
            for r in range(size):
                row = []
                for c in range(size):
                    if r != position[0] and c != position[1]:
                        row.append(data[r][c])
                if row: cut.append(row)
            return Matrix.determinant_static(cut)

    def cofactor(self, position):
        return (1 if (position[0] + position[1]) % 2 == 0 else -1) * self.minor(position)

    @staticmethod
    def cofactor_static(data, position):
        return (1 if (position[0] + position[1]) % 2 == 0 else -1) * Matrix.minor_static(data, position)

    def adjoint(self):
        data = self._data
        result = []
        for r in range(len(data)):
            row = []
            for c in range(len(data[0])):
                row.append(Matrix.cofactor_static(data, (r+1, c+1)))
            result.append(row)
        return Matrix.transpose_static(result)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Matrix calculator")
    root.iconbitmap("calculator.ico")
    root.geometry("400x200+300+200")
    
    tk.Label(master=root, text="Select the option" , font=("", 20)).grid(row=0, column=0, pady=20)
    menu = tk.Frame(master=root)
    tk.Button(master=menu, width=8, text="add", cursor="trek", font=("", 12), command=lambda:add_or_minus("+")).grid(row=0, column=0)
    tk.Button(master=menu, width=8, text="subtract", cursor="trek", font=("", 12), command=lambda:add_or_minus("-")).grid(row=0, column=1)
    tk.Button(master=menu, width=8, text="multiply", cursor="trek", font=("", 12), command=lambda:new_window("multiply")).grid(row=0,column=2)
    tk.Button(master=menu, width=8, text="det", cursor="trek", font=("", 12), command=lambda:new_window("det")).grid(row=0, column=3)
    tk.Button(master=menu, width=8, text="inverse", cursor="trek", font=("", 12), command=lambda:new_window("inverse")).grid(row=1, column=0)
    tk.Button(master=menu, width=8, text="minor", cursor="trek", font=("", 12), command=lambda:new_window("minor")).grid(row=1, column=1)
    tk.Button(master=menu, width=8, text="cofactor", cursor="trek", font=("", 12), command=lambda:new_window("cofactor")).grid(row=1, column=2)
    tk.Button(master=menu, width=8, text="adjoint", cursor="trek", font=("", 12), command=lambda:new_window("adjoint")).grid(row=1, column=3)
    menu.grid(row=1, column=0)
    root.columnconfigure(0, weight=1, minsize=100)
    root.minsize(330, 140)
    root.maxsize(500, 250)

    def add_or_minus(operator:str):
        window = tk.Toplevel(root)
        window.title("add" if operator == "+" else "subtract")
        window.geometry("300x400")
        window.minsize(300, 400)
        window.maxsize(400, 490)
        tk.Label(master=window, text="type your input below", font=("Arial", 20), fg="blue").grid(row=0, column=0, columnspan=3)
        frm_dim = tk.Frame(master=window)
        nrow, ncolumn  = tk.Entry(frm_dim, width=3), tk.Entry(frm_dim, width=3)
        nrow.grid(row=0, column=0)
        tk.Label(frm_dim, text="x", font=("", 10)).grid(row=0, column=1)
        ncolumn.grid(row=0, column=2)
        dimension = (nrow, ncolumn)
        frm_dim.grid(row=1, column=1)
        btn_dim = tk.Button(master=window, text="Okay",
        command=lambda: create_inp_mat(int(dimension[0].get()), int(dimension[1].get())))
        btn_dim.grid(row=2, column=1)
        mat_input = []
        submit_mat = tk.Button(master=window, text="Okay", width=5, height=1, command=lambda:show_output(operator))
        def create_inp_mat(row, column):
            nonlocal mat_input
            left, right = tk.Frame(master=window), tk.Frame(master=window)
            for master in (left, right):
                mat = []
                for r in range(row):
                    each_row = []
                    for c in range(column):
                        ent = tk.Entry(master=master, width=3)
                        ent.grid(row=r, column=c, padx=6, pady=6)
                        each_row.append(ent)
                    mat.append(each_row)
                mat_input.append(mat)
            left.grid(row=3, column=0)
            tk.Label(master=window, text=operator, font=("", 30)).grid(row=3, column=1)
            right.grid(row=3, column=2)
            submit_mat.grid(row=4, column=1)
        
        def show_output(operator):
            nonlocal mat_input
            A, B = [], []
            for r in mat_input[0]:
                row = []
                for c in r:
                    row.append(int(c.get()))
                A.append(row)
            for r in mat_input[1]:
                row = []
                for c in r:
                    row.append(int(c.get()))
                B.append(row)
            A, B = Matrix(A), Matrix(B)
            result = A + B if operator == "+" else A - B
            result = tk.Label(master=window, text=str(result), font=("Consolas", 20))
            result.grid(row=5, column=1)
        window.mainloop()

    root.mainloop()
import matplotlib.pyplot as plt


def nextDay(S, I, R, beta, delta, gamma):
	next_S = stayPositive(S - beta * I * S + gamma * R)
	next_I = stayPositive(I + beta * I * S - delta * I)
	next_R = stayPositive(R + delta * I - gamma * R)
	next_SIR = (next_S, next_I, next_R)
	return next_SIR

def stayPositive(number):
	if number >= 0:
		output = number
	else:
		output = 0
	return output

def printline():
	print("-" * 45)




import tkinter as tk


def makeForm(master):
    def plot_chart():
        s0_v = float(s0.get())
        i0_v = float(i0.get())
        r0_v = float(r0.get())
        beta_v = float(beta.get())
        delta_v = float(delta.get())
        gamma_v = float(gamma.get())
        day_v = int(days.get())

        print(s0_v, i0_v, r0_v)

        S = [s0_v]
        I = [i0_v]
        R = [r0_v]
        T = [0]

        for t in range(1, day_v + 1):
                latest_S = S[-1]
                latest_I = I[-1]
                latest_R = R[-1]
                next_SIR = nextDay(latest_S, latest_I, latest_R, beta_v, delta_v, gamma_v)
                S.append(next_SIR[0])
                I.append(next_SIR[1])
                R.append(next_SIR[2])
                T.append(t)

        plt.clf();
        plt.plot(T, S, label='Susceptible')
        plt.plot(T, I, label='Infected')
        plt.plot(T, R, label='Recovered')
        plt.xlabel('Days')
        plt.ylabel('Million')
        plt.title("Disease Spread Model")
        plt.legend()
        plt.show()
        #end scope of function

    tk.Label(master, text="Enter a number of S(0)").grid(row=0)
    tk.Label(master, text="Enter a number of I(0)").grid(row=1)
    tk.Label(master, text="Enter a number of R(0)").grid(row=2)

    tk.Label(master, text="Enter a number of beta").grid(row=3)
    tk.Label(master, text="Enter a number of delta").grid(row=4)
    tk.Label(master, text="Enter a number of gamma").grid(row=5)
    tk.Label(master, text="Enter a number of days").grid(row=6)

    s0 = tk.Entry(master)
    s0.insert(0, 60.0)

    i0 = tk.Entry(master)
    i0.insert(0, 0.1)

    r0 = tk.Entry(master)
    r0.insert(0,0)

    beta = tk.Entry(master)
    beta.insert(0, 0.0045)

    delta = tk.Entry(master)
    delta.insert(0, 0.0001)

    gamma = tk.Entry(master)
    gamma.insert(0, 0.005)

    #days = tk.Entry(master)
    days = tk.Scale(master, from_=1, to=365, orient=tk.HORIZONTAL)

    s0.grid(row=0, column=1)
    i0.grid(row=1, column=1)
    r0.grid(row=2, column=1)
    beta.grid(row=3, column=1)
    delta.grid(row=4, column=1)
    gamma.grid(row=5, column=1)
    days.grid(row=6, column=1)

    tk.Button(master,
              text='Quit',
              command=master.quit).grid(row=7,
                                        column=0,
                                        sticky=tk.W,
                                        pady=4)
    tk.Button(master, text='Plot', command=plot_chart).grid(row=7,
                                                                   column=1,
                                                                   sticky=tk.W,
                                                                   pady=4)


if __name__ == '__main__':
    master = tk.Tk()
    makeForm(master)
    master.mainloop()
    #tk.mainloop()

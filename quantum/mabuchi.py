

chi_qs_KHz = 30
kerr_Hz = 1

chi_qs = 1e-6* (2*np.pi)*chi_qs_KHz
kerr = 1e-9*(2*np.pi)*kerr_Hz * 1

def simulate_qc_pulse_full_loss(gamma,delta, alpha0, psi0, dt=1, plot=True):
    N = psi0.dims[0][0]

    a = qt.destroy(N)
    
    H_kerr = 0.5*kerr*a.dag()*a.dag()*a*a + kerr*alpha0*a.dag()*a*a + kerr*alpha0*a.dag()*a.dag()*a + 0.5*kerr*alpha0**2*(a.dag()*a.dag() + a*a)
    H0 = -delta*a.dag()*a - chi_qs*a.dag()*a*q.dag()*q - chi_qs*alpha0*(a.dag()+a)*q.dag()*q - (Ec/2.0)*q.dag()**2 * q**2 - H_kerr + max_N_loss
    HqI = q + q.dag()
    HqQ = 1j*(q.dag() - q)
    Hcs = [HqI, HqQ]
    
    
    ts = np.arange(0,len(gammaI)*dt, dt)
    SqI = qt.interpolate.Cubic_Spline(ts[0], ts[-1], gammaI)
    SqQ = qt.interpolate.Cubic_Spline(ts[0], ts[-1], gammaQ)
    
    H = [H0,[HqI,SqI],[HqQ,SqQ]]
    
    # loss operator setup
    c_ops = [np.sqrt(qubit_Gamma_down)*q, np.sqrt(qubit_Gamma_up)*q.dag(), np.sqrt(qubit_dephasing)*q.dag()*q, np.sqrt(kappa_cavity)*a]#, np.sqrt(cavity_dephasing)*a.dag()*a]
    
    result = qt.mesolve(H,psi0,ts,c_ops,[], options = myoptions)
    
    if plot:
        plot_wigner(result.states[-1])
        plt.figure(figsize = (10,8))
        x = np.array([qt.expect(sx, result.states[i]) for i in range(len(ts))])
        y = np.array([qt.expect(sy, result.states[i]) for i in range(len(ts))])
        z = np.array([qt.expect(sz, result.states[i]) for i in range(len(ts))])
        plt.plot(ts,x,label='<sx>')
        plt.plot(ts,y,label='<sy>')
        plt.plot(ts,z,label='<sz>')
        plt.plot(ts,x**2 + y**2 + z**2,label='Purity')
        plt.xlabel('t (ns)')
        plt.legend()
        plt.show()
        plt.figure(figsize = (10,8))
        plt.plot(ts,[qt.expect(a.dag()*a, result.states[i]) for i in range(len(ts))],label='<n>')
        plt.legend()
        plt.show()
        plt.figure(figsize = (10,8))
        plt.plot(ts,[qt.expect((a.dag() + a)/2, result.states[i]) for i in range(len(ts))],label='<I>')
        plt.plot(ts,[qt.expect(1j*(a.dag() - a)/2, result.states[i]) for i in range(len(ts))],label='<Q>')
        plt.xlabel('t (ns)')
        plt.legend()
        plt.show()
    
    return result.states
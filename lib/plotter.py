import matlab.engine
import numpy as np
from scipy import signal as sig
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def zpkload(opt, in_stage, in_dof, out_stage, out_dof):
    if 'TM' in opt:
        inv = 'inj'+in_stage+in_dof
        if out_stage == 'TM':
            outv = 'disp'+'TM'+out_dof
        elif out_stage=='IM':
            outv = 'PS_'+'IM'+out_dof
        elif out_stage=='MN':
            outv = 'OpLev_'+'MN'+out_dof
        else:
            outv = 'LVDT_'+out_stage+out_dof
    else:
        inv = 'act'+in_dof+in_stage
        if out_stage == 'TM':
            outv = out_dof+'TM'
        elif out_stage=='IM':
            outv = 'OSEM_'+out_dof+'IM'
        else:
            outv = 'LVDT_'+out_dof+out_stage

    eng = matlab.engine.start_matlab()
    eng.addpath('/kagra/Dropbox/Subsystems/VIS/Scripts/SuspensionControlModel/utility')
    ans = eng.model2fotonzpk_VISapp(opt,inv,outv,nargout=4)

    zpk_txt = ans[0]
    zz=np.array(ans[1])
    pp=np.array(ans[2])
    kk=ans[3]

    zz = zz.T
    pp = pp.T

    zz = zz[0]
    pp = pp[0]

    return zpk_txt,zz,pp,kk

def plotzpk(zz,pp,kk, legend_txt,figval=1):
    sys = sig.ZerosPolesGain(zz,-1*pp,kk)
    freq = np.logspace(-2,2,500)
    freq, mag, phase = sig.bode(sys,freq)
    mag = 10.0**(mag/20.0)
    phase = ( phase + 180.0 ) % (360.0 ) - 180.0

    fig = plt.figure(figval)
    plt.subplot(211)
    plt.loglog(freq,mag,label=legend_txt)
    plt.legend()
    plt.grid(True)
    plt.ylabel('Gain')
    plt.subplot(212)
    plt.semilogx(freq,phase)
    plt.grid(True)
    plt.ylim([-190,190])
    plt.ylabel('Phase [deg]')
    plt.xlabel('Frequency [Hz]')

    figurename = 'result'+str(figval)+'.png'
    fig.savefig('./static/'+figurename)
    return figurename

def plotTFdata(filename,chA,chB,legend_txt,figval=1):
    eng = matlab.engine.start_matlab()
    eng.addpath('/kagra/Dropbox/Subsystems/VIS/Scripts/SuspensionControlModel/utility')
    ans = eng.DttTFplot_VISapp(filename,chA,chB,nargout=4)
    status = ans[0]

    legend_txt = legend_txt

    if status == 0:
        freq = ans[1]
        mag = ans[2]
        phase = ans[3]
        fig = plt.figure(figval)
        plt.subplot(211)
        plt.loglog(freq,mag,label=legend_txt)
        plt.legend()
        plt.grid(True)
        plt.ylabel('Gain')
        plt.subplot(212)
        plt.semilogx(freq,phase)
        plt.grid(True)
        plt.ylabel('Phase [deg]')
        plt.xlabel('Frequency [Hz]')

        figurename = 'result'+str(figval)+'.png'
        fig.savefig('./static/'+figurename)
    else:
        fig = plt.figure(figval)
        figurename = 'result'+str(figval)+'.png'
        fig.savefig('./static/'+figurename)
    return status, figurename

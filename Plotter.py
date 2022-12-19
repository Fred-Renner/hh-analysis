#!/usr/bin/env python3
# from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib import ticker
import mplhep as hep
from h5py import File, Group, Dataset
import os
import logging
import argparse
import PlottingTools as tools

# quick and dirty color log
logging.basicConfig(level=logging.INFO)
logging.addLevelName(
    logging.INFO, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.INFO)
)

matplotlib.font_manager._rebuild()
plt.style.use(hep.style.ATLAS)


parser = argparse.ArgumentParser()
parser.add_argument("--histFile", type=str, default=None)
args = parser.parse_args()

# fmt: off
histFileBkg = []
# histFile = "/lustre/fs22/group/atlas/freder/hh/run/histograms/hists-user.frenner.HH4b.2022_11_25_.601479.PhPy8EG_HH4b_cHHH01d0.e8472_s3873_r13829_p5440_TREE.h5"
# histFile = "/lustre/fs22/group/atlas/freder/hh/run/histograms/hists-user.frenner.HH4b.2022_11_25_.601480.PhPy8EG_HH4b_cHHH10d0.e8472_s3873_r13829_p5440_TREE.h5"
histFile = "/lustre/fs22/group/atlas/freder/hh/run/histograms/hists-MC20-signal-1cvv1cv1.h5"
histFileBkg = "/lustre/fs22/group/atlas/freder/hh/run/histograms/hists-MC20-bkg-ttbar.h5"

# fmt: on

if args.histFile:
    histFile = args.histFile

# make plot directory
filename = histFile.split("/")
filename = str(filename[-1]).replace(".h5", "")
logging.info("make plots for " + filename)
plotPath = "/lustre/fs22/group/atlas/freder/hh/run/histograms/plots-" + filename + "/"
if not os.path.isdir(plotPath):
    os.makedirs(plotPath)


def getHist(file, name):
    # access [1:-1] to remove underflow and overflow bins
    h = file[name]["histogram"][1:-1]
    bins = file[name]["edges"]
    return h, bins


def trigger_leadingLargeRpT():
    triggerRef_leadingLargeRpT = file["triggerRef_leadingLargeRpT"]["histogram"][1:-1]
    trigger_leadingLargeRpT = file["trigger_leadingLargeRpT"]["histogram"][1:-1]
    trigger_leadingLargeRpT_err = tools.getEfficiencyErrors(
        passed=trigger_leadingLargeRpT, total=triggerRef_leadingLargeRpT
    )
    # normalize + cumulative
    # edges = file["triggerRef_leadingLargeRpT"]["edges"]
    # counts = file["triggerRef_leadingLargeRpT"]["histogram"][1:-1].astype(int)
    # values = np.repeat((edges[:-1] + edges[1:]) / 2.0, counts)
    # triggerRef_leadingLargeRpT = np.array(
    #     plt.hist(values, edges, density=True, cumulative=True)[0], dtype=float
    # )

    # edges = file["trigger_leadingLargeRpT"]["edges"]
    # counts = file["trigger_leadingLargeRpT"]["histogram"][1:-1].astype(int)
    # values = np.repeat((edges[:-1] + edges[1:]) / 2.0, counts)
    # trigger_leadingLargeRpT = np.array(
    #     plt.hist(values, edges, density=True, cumulative=True)[0], dtype=float
    # )

    plt.figure()
    plt.grid()

    hep.histplot(
        trigger_leadingLargeRpT / triggerRef_leadingLargeRpT,
        file["triggerRef_leadingLargeRpT"]["edges"],
        histtype="errorbar",
        yerr=trigger_leadingLargeRpT_err,
        solid_capstyle="projecting",
        capsize=3,
        # density=True,
        alpha=0.75,
    )

    hep.atlas.text(" Simulation", loc=1)
    # hep.atlas.set_ylabel("Cumulative Trigger eff.")
    hep.atlas.set_ylabel("Trigger eff.")
    hep.atlas.set_xlabel("Leading Large R Jet p$_T$ $[GeV]$ ")
    ax = plt.gca()
    ax.xaxis.set_major_formatter(tools.OOMFormatter(3, "%1.1i"))
    ax.get_xaxis().get_offset_text().set_position((1.09, 0))
    # ax.set_ylim([0.8, 1.05])
    # ax.set_xlim([0.8, 2500_000])
    plt.tight_layout()
    plt.legend(loc="upper right")
    plt.savefig(plotPath + "trigger_leadingLargeRpT.pdf")
    plt.close()


def trigger_leadingLargeRm():
    # normalize + cumulative
    triggerRef_leadingLargeRm = file["triggerRef_leadingLargeRm"]["histogram"][1:-1]
    trigger_leadingLargeRm = file["trigger_leadingLargeRm"]["histogram"][1:-1]
    trigger_leadingLargeRm_err = tools.getEfficiencyErrors(
        passed=trigger_leadingLargeRm, total=triggerRef_leadingLargeRm
    )
    # edges = file["triggerRef_leadingLargeRm"]["edges"]
    # counts = file["triggerRef_leadingLargeRm"]["histogram"][1:-1].astype(int)
    # values = np.repeat((edges[:-1] + edges[1:]) / 2.0, counts)
    # triggerRef_leadingLargeRm = np.array(
    #     plt.hist(values, edges, density=True, cumulative=True)[0], dtype=float
    # )

    # edges = file["trigger_leadingLargeRm"]["edges"]
    # counts = file["trigger_leadingLargeRm"]["histogram"][1:-1].astype(int)
    # values = np.repeat((edges[:-1] + edges[1:]) / 2.0, counts)
    # trigger_leadingLargeRm = np.array(
    #     plt.hist(values, edges, density=True, cumulative=True)[0], dtype=float
    # )

    plt.figure()
    hep.histplot(
        trigger_leadingLargeRm / triggerRef_leadingLargeRm,
        file["trigger_leadingLargeRm"]["edges"],
        histtype="errorbar",
        yerr=trigger_leadingLargeRm_err,
        solid_capstyle="projecting",
        capsize=3,
        # density=True,
        alpha=0.75,
    )

    hep.atlas.text(" Simulation", loc=1)
    # hep.atlas.set_ylabel("Cumulative Trigger eff.")
    hep.atlas.set_ylabel("Trigger eff.")
    hep.atlas.set_xlabel("Leading Large R Jet Mass $[GeV]$ ")
    ax = plt.gca()
    ax.set_ylim([0, 2])

    ax.xaxis.set_major_formatter(tools.OOMFormatter(3, "%1.1i"))
    ax.get_xaxis().get_offset_text().set_position((1.09, 0))
    plt.grid()

    plt.tight_layout()
    plt.legend(loc="upper right")
    plt.savefig(plotPath + "trigger_leadingLargeRm.pdf")
    plt.close()


def accEff_mhh():
    mhh = file["mhh"]["histogram"][1:-1]
    keys = [
        "nTriggerPass_mhh",
        "nTwoLargeR_mhh",
        "nTwoSelLargeR_mhh",
        "btagLow_1b1j_mhh",
        "btagLow_2b1j_mhh",
        "btagLow_2b2j_mhh",
        "btagHigh_1b1b_mhh",
        "btagHigh_2b1b_mhh",
        "btagHigh_2b2b_mhh",
    ]
    hists = []
    for key in keys:
        hists.append(file[key]["histogram"][1:-1])
    hists_cumulative, hists_cumulative_err = tools.CumulativeEfficiencies(
        hists, baseline=mhh, stopCumulativeFrom=4
    )
    labels = [
        "passed Trigger",
        "≥2 LargeR",
        "$p_T$>250 GeV, $|\eta\| < 2.0$",
        "btagLow 1b1j",
        "btagLow 2b1j",
        "btagLow 2b2j",
        "btagHigh 1b1b",
        "btagHigh 2b1b",
        "btagHigh 2b2b",
    ]
    plt.figure()

    for i, (h, err, label) in enumerate(
        zip(hists_cumulative, hists_cumulative_err, labels)
    ):
        hep.histplot(
            h,
            file["nTriggerPass_mhh"]["edges"],
            histtype="errorbar",
            label=label,
            yerr=err,
            alpha=0.7,
            solid_capstyle="projecting",
            capsize=3,
            color="C{}".format(i),
        )

    hep.atlas.text(" Simulation", loc=1)
    hep.atlas.set_ylabel("Acc x Efficiency")
    hep.atlas.set_xlabel("$m_{hh}$ $[GeV]$ ")
    ax = plt.gca()
    ax.xaxis.set_major_formatter(tools.OOMFormatter(3, "%1.1i"))
    ax.get_xaxis().get_offset_text().set_position((1.09, 0))
    ax.set_ylim([0, 1.4])
    plt.legend(loc="upper left", bbox_to_anchor=(0.01, 0.9))
    hep.rescale_to_axessize
    plt.tight_layout()
    plt.savefig(plotPath + "accEff_mhh.pdf")
    plt.close()


def leadingLargeRpT():
    plt.figure()
    leadingLargeRpT = file["leadingLargeRpT"]["histogram"][1:-1]
    leadingLargeRpT_trigger = file["leadingLargeRpT_trigger"]["histogram"][1:-1]
    err = tools.getEfficiencyErrors(
        passed=leadingLargeRpT_trigger, total=leadingLargeRpT
    )
    hep.histplot(
        leadingLargeRpT / leadingLargeRpT_trigger,
        file["leadingLargeRpT"]["edges"],
        histtype="errorbar",
        yerr=err,
        density=False,
        # alpha=0.75,
        label=["triggerRef_leadingLargeRpT", "trigger_leadingLargeRpT"],
    )
    hep.atlas.text(" Simulation", loc=1)
    hep.atlas.set_ylabel("Events")
    hep.atlas.set_xlabel("Leading Large R Jet p$_T$ $[GeV]$ ")
    ax = plt.gca()
    ax.get_xaxis().get_offset_text().set_position((1.09, 0))
    ax.xaxis.set_major_formatter(tools.OOMFormatter(3, "%1.1i"))
    plt.tight_layout()
    plt.legend(loc="upper right")
    plt.savefig(plotPath + "leadingLargeRpT.pdf")
    plt.close()


def mhh():
    plt.figure()
    mhh = file["mhh"]["histogram"][1:-1]
    # truth_mhh = file["truth_mhh"]["histogram"][1:-1]
    # trigger_leadingLargeRm_err = tools.getEfficiencyErrors(
    #     passed=mhh, total=truth_mhh
    # )
    hep.histplot(
        mhh,  # / truth_mhh,
        file["mhh"]["edges"],
        histtype="errorbar",
        yerr=True,
        solid_capstyle="projecting",
        capsize=3,
        # label=["truth", "reco"]
        # alpha=0.75,
    )
    hep.atlas.text(" Simulation", loc=1)
    hep.atlas.set_ylabel("Events")
    hep.atlas.set_xlabel("$m_{hh}$ $[GeV]$ ")
    ax = plt.gca()
    # ax.set_yscale("log")
    ax.xaxis.set_major_formatter(tools.OOMFormatter(3, "%1.1i"))
    ax.get_xaxis().get_offset_text().set_position((1.09, 0))
    plt.legend(loc="upper right")
    # hep.yscale_legend()
    plt.tight_layout()
    plt.savefig(plotPath + "mhh.pdf")
    plt.close()


def massplane_77():
    plt.figure()
    histValues = file["massplane_77"]["histogram"][1:-1, 1:-1]
    hep.hist2dplot(
        histValues,
        xbins=file["massplane_77"]["edges"][0][1:-1],
        ybins=file["massplane_77"]["edges"][1][1:-1],
    )
    txt = hep.atlas.text(" Simulation", loc=1)
    txt[0]._color = "white"
    txt[1]._color = "white"
    hep.atlas.set_ylabel("$m_{h2}$ $[GeV]$ ")
    hep.atlas.set_xlabel("$m_{h1}$ $[GeV]$ ")
    ax = plt.gca()
    ax.get_xaxis().get_offset_text().set_position((1.09, 0))
    ax.xaxis.set_major_formatter(tools.OOMFormatter(3, "%1.1i"))
    ax.yaxis.set_major_formatter(tools.OOMFormatter(3, "%1.1i"))
    ax.set_aspect("equal")
    plt.tight_layout()
    # plt.legend(loc="upper right")
    plt.savefig(plotPath + "massplane.pdf")
    plt.close()


def vrJetEfficiencyBoosted():
    plt.figure()
    vals = file["vrJetEfficiencyBoosted"]["histogram"][1:-1]
    hep.histplot(
        [vals[1] / (vals[0] + vals[1]), vals[3] / (vals[2] + vals[3])],
        file["vrJetEfficiencyBoosted"]["edges"][:3],
        label="vrJetEfficiencyBoosted",
        density=False,
        alpha=0.75,
    )
    hep.atlas.text(" Simulation", loc=1)
    nEvents = vals[2] + vals[3]
    hep.atlas.set_ylabel("VR jets efficiency")
    hep.atlas.set_xlabel("leading H (bin 0), subleading H (bin 1)")
    ax = plt.gca()
    ax.get_xaxis().get_offset_text().set_position((1.09, 0))
    # ax.set_xticks(file[hist]["edges"])
    plt.tight_layout()
    # plt.legend(loc="upper right")
    plt.savefig(plotPath + "vrJetEfficiencyBoosted_0p2.pdf")
    plt.close()


def mh1_ratio():
    plt.figure()
    signal, edges = getHist(file, "mh1")
    bkg, edges2 = getHist(fileBkg, "mh1")

    fig, (ax, rax) = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(8, 8),
        gridspec_kw={"height_ratios": (3, 1)},
        sharex=True,
    )

    hep.histplot(
        [signal, bkg],
        edges,
        stack=True,
        histtype="fill",
        # yerr=True,
        label=["SM Signal", "t$\overline{t}$"],
        ax=ax,
    )
    ratio_err = tools.getEfficiencyErrors(passed=signal, total=bkg)

    hep.histplot(
        signal / bkg,
        edges,
        stack=True,
        histtype="errorbar",
        yerr=ratio_err,
        label=["SM Signal", "t$\overline{t}$"],
        ax=rax,
        color="Black",
    )
    # hep.cms.label(data=True, lumi=59.97, year=2018, loc=0)
    fig.subplots_adjust(hspace=0.07)
    ax.set_ylabel("Events")
    rax.set_ylabel("Signal/Background")
    hep.atlas.set_xlabel("$m_{h1}$ $[GeV]$ ")
    rax.get_xaxis().get_offset_text().set_position((1.09, 0))

    plt.tight_layout()
    ax.legend(loc="upper right")
    plt.savefig(plotPath + "mh1_ratio.pdf")
    plt.close()


with File(histFile, "r") as file:
    # trigger_leadingLargeRpT()
    # trigger_leadingLargeRm()
    # accEff_mhh()
    # leadingLargeRpT()
    # mhh()
    # massplane_77()
    if histFileBkg:
        with File(histFileBkg, "r") as fileBkg:
            mh1_ratio()

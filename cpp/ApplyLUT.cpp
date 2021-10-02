// 应用LUT

#include <iostream>
#include <string>

#include "lut.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>

using namespace std;
namespace py = pybind11;

#define OPEN_MP_THREAD_NUM 128

// #define DEBUG

class ApplyLUT
{
public:

    ApplyLUT() {}

    ApplyLUT(string cube_file_path_)
    {
        this->cube_file_path = cube_file_path_;
        this->lut = octoon::image::detail::basic_lut<float>::parse(this->cube_file_path);
        #ifdef DEBUG
            printf("load cube file Done.\n");
        #endif
    }

    // Tensor 不被正式支持, 输入LUT需要拉成 N，3 的矩阵
    // TODO: 测试
    ApplyLUT(int dimsz, Eigen::MatrixXd vec_)
    {
        vector<float> vlut;
        int sz = vec_.size()/3;
        for(int i=0;i<sz;i++)
            for(int j=0;j<3;j++)
                vlut.push_back(vec_(i,j));
        this->lut.create(dimsz,vlut);
    }

    // Tensor 不被正式支持, 输入图片需要拉成 N，3 的矩阵
    Eigen::MatrixXd apply_lut_1d(Eigen::MatrixXd img)
    {
        Eigen::MatrixXd out = img;
        // printf("out.size: %d\n",out.size());
        int n = out.size()/3;
        #pragma omp parallel for num_threads( OPEN_MP_THREAD_NUM )
        for(int i=0;i<n;i++)
        {
            float r = out(i,0);
            float g = out(i,1);
            float b = out(i,2);
            auto nrgb = lut.lookup(r,g,b);
            out(i,0) = nrgb[0];
            out(i,1) = nrgb[1];
            out(i,2) = nrgb[2];
        }
        return out;
    }

    #ifdef DEBUG
    void debug()
    {
        printf("this is debug function!");
    }
    #endif

public:
    string cube_file_path;
    // Matrix3d cube;
    octoon::image::detail::basic_lut<float> lut;
};

PYBIND11_MODULE(ApplyLUT, m)
{
    py::class_<ApplyLUT>(m,"ApplyLUT")
        .def(py::init<>())
        .def(py::init<const std::string &>())
        .def(py::init<int,Eigen::MatrixXd>())
        .def("apply_lut_1d",&ApplyLUT::apply_lut_1d)
        #ifdef DEBUG
        .def("debug",&ApplyLUT::debug)
        #endif
        ;
}
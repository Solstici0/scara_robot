import math
import pytest
import scara.tools.kinematics as kin

def test_correct_import():
    assert  330.15  == kin.r1
    assert 336.0 == kin.r2

def test_estiradito_is_0_in_x():
    ik_dict = kin.inverse_kin(0,330.15+336.0)
    assert ik_dict["hombro"] == math.pi/2
    assert ik_dict["codo"] == 0

def test_max_x():
    ik_dict = kin.inverse_kin(330.15+336.0,0)
    assert ik_dict["hombro"] == 0
    assert ik_dict["codo"] == 0

def test_general_case():
    expected_hombro  = math.pi/4
    expected_codo = math.pi/4
    given_x, given_y = kin.direct_kin(expected_hombro,expected_codo)
    ik_dict = kin.inverse_kin(given_x,given_y)
    assert expected_hombro == pytest.approx(ik_dict["hombro"])
    assert expected_codo == pytest.approx(ik_dict["codo"])


def test_general_case_left():
    expected_hombro  = math.pi/4
    expected_codo = -1*math.pi/4
    given_x, given_y = kin.direct_kin(expected_hombro,expected_codo)
    ik_dict = kin.inverse_kin(given_x,given_y,'left')
    assert expected_hombro == pytest.approx(ik_dict["hombro"])
    assert expected_codo == pytest.approx(ik_dict["codo"])

def print_report_ik(x,y,expected_hombro,expected_codo,ik_dict):
    format_string = 'x, y = %2f, %2f \n'\
                                +'          expected , actual\n'\
                                +'hombro | %2f, %2f\n'\
                                +'codo   | %2f, %2f\n'
    if ik_dict['hombro']:
        actual_hombro  = ik_dict['hombro']
    else:
        actual_hombro = 666.0
    if ik_dict['codo']:
        actual_codo = ik_dict['codo']
    else:
        actual_codo = 666.0
    result_string = format_string % (x,y,
                                    expected_hombro,actual_hombro,
                                    expected_codo,actual_codo)
    print(result_string)

def test_a_lot_of_cases():
    number_of_points = 1000
    theta1_step_size = (kin.maxtheta1[1]-kin.maxtheta1[0])/(number_of_points-1)
    theta2_step_size = (kin.maxtheta2[1]-kin.maxtheta2[0])/(number_of_points-1)
    theta1_list = [kin.maxtheta1[0] + i*theta1_step_size for i in range(number_of_points)]
    theta2_list = [kin.maxtheta2[0] + i*theta2_step_size for i in range(number_of_points)]
    for expected_hombro in theta1_list:
        for expected_codo in theta2_list:
            x,y = kin.direct_kin(expected_hombro,expected_codo)
            if expected_codo<0:
                ik_dict = kin.inverse_kin(x,y,'left')
            else:
                ik_dict = kin.inverse_kin(x,y,'right')
            if expected_hombro == pytest.approx(ik_dict['hombro']):
                assert True
            else:
                print_report_ik(x,y,expected_hombro,expected_codo,ik_dict)
                assert False
            if expected_codo == pytest.approx(ik_dict['codo']):
                assert True
            else:
                print_report_ik(x,y,expected_hombro,expected_codo,ik_dict)
                assert False           

